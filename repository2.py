"""
repository.py
====
Repositorio de datos y cálculos del Dashboard de Rendimiento Académico.
Versión simplificada: solo pandas, sin polars, sin carga de archivos externos.

Dependencias: pandas, numpy.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

# ---- Constantes ---- #

RUTA_BASE:       Path  = Path(__file__).resolve().parent
ARCHIVO_ALUMNOS: Path  = RUTA_BASE / "Alumnos.csv"
ARCHIVO_NOTAS:   Path  = RUTA_BASE / "Notas.csv"

NOTA_APROBADO:    float = 5.0
GRUPO_DESCONOCIDO: str  = "Sin grupo"
TODOS:             str  = "Todos"

COLUMNAS_ASIGNATURA = [
    "asignatura", "alumnos_evaluados", "nota_media",
    "nota_maxima", "nota_minima", "porcentaje_aprobados",
]
COLUMNAS_ALUMNO = [
    "id_alumno", "nombre", "curso", "grupo",
    "nota_media", "asignaturas_evaluadas", "asignaturas_aprobadas",
]


# ---- 1. Carga y limpieza ---- #

def cargar_alumnos() -> pd.DataFrame:
    df = pd.read_csv(ARCHIVO_ALUMNOS)
    df["id_alumno"] = pd.to_numeric(df["id_alumno"], errors="coerce").astype("Int64")
    df["nombre"]    = df["nombre"].astype(str).str.strip().str.title()
    df["edad"]      = pd.to_numeric(df["edad"], errors="coerce").astype("Int64")
    df["curso"]     = df["curso"].astype(str).str.strip()
    df["grupo"]     = (
        df["grupo"].astype("string").str.strip()
        .replace({"": pd.NA, "nan": pd.NA, "None": pd.NA})
        .fillna(GRUPO_DESCONOCIDO)
    )
    return df.dropna(subset=["id_alumno"]).reset_index(drop=True)


def cargar_notas() -> pd.DataFrame:
    df = pd.read_csv(ARCHIVO_NOTAS)
    df["id_alumno"]  = pd.to_numeric(df["id_alumno"],  errors="coerce").astype("Int64")
    df["evaluacion"] = pd.to_numeric(df["evaluacion"], errors="coerce").astype("Int64")
    df["nota"]       = pd.to_numeric(df["nota"],       errors="coerce").clip(0, 10)
    df["asignatura"] = df["asignatura"].astype(str).str.strip()
    return df.dropna(subset=["id_alumno", "nota"]).reset_index(drop=True)


def construir_dataset(alumnos: pd.DataFrame, notas: pd.DataFrame) -> pd.DataFrame:
    datos = notas.merge(alumnos, on="id_alumno", how="left")
    datos["nombre"]   = datos["nombre"].fillna("Desconocido")
    datos["curso"]    = datos["curso"].fillna("Sin curso")
    datos["grupo"]    = datos["grupo"].fillna(GRUPO_DESCONOCIDO)
    datos["aprobado"] = datos["nota"] >= NOTA_APROBADO
    columnas = ["id_nota", "id_alumno", "nombre", "edad", "curso", "grupo",
                "asignatura", "evaluacion", "nota", "aprobado"]
    return datos[[c for c in columnas if c in datos.columns]].reset_index(drop=True)


def cargar_datos():
    """Punto de entrada único: devuelve (alumnos, notas, dataset)."""
    alumnos = cargar_alumnos()
    notas   = cargar_notas()
    return alumnos, notas, construir_dataset(alumnos, notas)


# ---- 2. Filtros ---- #

def obtener_opciones(datos: pd.DataFrame) -> dict:
    if datos.empty:
        return {"curso": [], "asignatura": [], "grupo": [], "evaluacion": []}
    return {
        "curso":      sorted(datos["curso"].dropna().unique().tolist()),
        "asignatura": sorted(datos["asignatura"].dropna().unique().tolist()),
        "grupo":      sorted(datos["grupo"].dropna().unique().tolist()),
        "evaluacion": sorted(datos["evaluacion"].dropna().unique().tolist()),
    }


def aplicar_filtros(datos, curso=None, asignatura=None, grupo=None, evaluacion=None):
    def es_todos(v):
        return v is None or v == TODOS or v == ""

    f = datos
    if not es_todos(curso):       f = f[f["curso"]      == curso]
    if not es_todos(asignatura):  f = f[f["asignatura"] == asignatura]
    if not es_todos(grupo):       f = f[f["grupo"]       == grupo]
    if not es_todos(evaluacion):  f = f[f["evaluacion"] == evaluacion]
    return f.reset_index(drop=True)


# ---- 3. KPIs ---- #

def calcular_kpis(datos: pd.DataFrame) -> dict:
    if datos.empty:
        return {"alumnos_evaluados": 0, "nota_media": 0.0,
                "nota_maxima": 0.0, "nota_minima": 0.0, "porcentaje_aprobados": 0.0}
    notas = datos["nota"].to_numpy(float)
    return {
        "alumnos_evaluados":   int(datos["id_alumno"].nunique()),
        "nota_media":          float(np.mean(notas)),
        "nota_maxima":         float(np.max(notas)),
        "nota_minima":         float(np.min(notas)),
        "porcentaje_aprobados": float(datos["aprobado"].mean() * 100),
    }


# ---- 4. Estadísticas agregadas (solo pandas) ---- #

def estadisticas_por_asignatura(datos: pd.DataFrame) -> pd.DataFrame:
    if datos.empty:
        return pd.DataFrame(columns=COLUMNAS_ASIGNATURA)
    r = datos.groupby("asignatura").agg(
        alumnos_evaluados=("id_alumno", "nunique"),
        nota_media=("nota", "mean"),
        nota_maxima=("nota", "max"),
        nota_minima=("nota", "min"),
        porcentaje_aprobados=("aprobado", lambda x: x.mean() * 100),
    ).reset_index().sort_values("nota_media", ascending=False)
    return r[COLUMNAS_ASIGNATURA].reset_index(drop=True)


def rendimiento_por_alumno(datos: pd.DataFrame) -> pd.DataFrame:
    if datos.empty:
        return pd.DataFrame(columns=COLUMNAS_ALUMNO)
    por_asig = datos.groupby(["id_alumno", "asignatura"])["nota"].mean().reset_index()
    por_asig.columns = ["id_alumno", "asignatura", "media_asignatura"]
    resumen = por_asig.groupby("id_alumno").agg(
        asignaturas_evaluadas=("asignatura", "nunique"),
        asignaturas_aprobadas=("media_asignatura", lambda x: (x >= NOTA_APROBADO).sum()),
        nota_media=("media_asignatura", "mean"),
    ).reset_index()
    identidad = datos[["id_alumno", "nombre", "curso", "grupo"]].drop_duplicates("id_alumno")
    r = identidad.merge(resumen, on="id_alumno", how="left").sort_values("nota_media", ascending=False)
    return r[COLUMNAS_ALUMNO].reset_index(drop=True)


def evolucion_por_evaluacion(datos: pd.DataFrame) -> pd.DataFrame:
    cols = ["evaluacion", "nota_media", "nota_maxima", "nota_minima",
            "porcentaje_aprobados", "num_notas"]
    if datos.empty:
        return pd.DataFrame(columns=cols)
    r = datos.groupby("evaluacion").agg(
        nota_media=("nota", "mean"),
        nota_maxima=("nota", "max"),
        nota_minima=("nota", "min"),
        porcentaje_aprobados=("aprobado", lambda x: x.mean() * 100),
        num_notas=("nota", "count"),
    ).reset_index().sort_values("evaluacion")
    return r[cols].reset_index(drop=True)


def evolucion_por_asignatura(datos: pd.DataFrame) -> pd.DataFrame:
    cols = ["evaluacion", "asignatura", "nota_media", "num_notas"]
    if datos.empty:
        return pd.DataFrame(columns=cols)
    r = datos.groupby(["evaluacion", "asignatura"]).agg(
        nota_media=("nota", "mean"),
        num_notas=("nota", "count"),
    ).reset_index().sort_values(["asignatura", "evaluacion"])
    return r[cols].reset_index(drop=True)


def estadisticas_por_grupo(datos: pd.DataFrame) -> pd.DataFrame:
    cols = ["grupo", "alumnos", "nota_media", "porcentaje_aprobados"]
    if datos.empty:
        return pd.DataFrame(columns=cols)
    r = datos.groupby("grupo").agg(
        alumnos=("id_alumno", "nunique"),
        nota_media=("nota", "mean"),
        porcentaje_aprobados=("aprobado", lambda x: x.mean() * 100),
    ).reset_index().sort_values("grupo")
    return r[cols].reset_index(drop=True)


def estadisticas_por_curso(datos: pd.DataFrame) -> pd.DataFrame:
    cols = ["curso", "alumnos", "nota_media", "porcentaje_aprobados"]
    if datos.empty:
        return pd.DataFrame(columns=cols)
    r = datos.groupby("curso").agg(
        alumnos=("id_alumno", "nunique"),
        nota_media=("nota", "mean"),
        porcentaje_aprobados=("aprobado", lambda x: x.mean() * 100),
    ).reset_index().sort_values("nota_media", ascending=False)
    return r[cols].reset_index(drop=True)


# ---- 5. Distribución ---- #

def resumen_distribucion(datos: pd.DataFrame) -> dict:
    if datos.empty:
        return {"media": 0.0, "mediana": 0.0, "desviacion": 0.0, "p25": 0.0, "p75": 0.0}
    notas = datos["nota"].to_numpy(float)
    return {
        "media":      float(np.mean(notas)),
        "mediana":    float(np.median(notas)),
        "desviacion": float(np.std(notas, ddof=1)) if notas.size > 1 else 0.0,
        "p25":        float(np.percentile(notas, 25)),
        "p75":        float(np.percentile(notas, 75)),
    }


def tabla_distribucion(datos: pd.DataFrame, intervalos: int = 10) -> pd.DataFrame:
    if datos.empty:
        return pd.DataFrame(columns=["intervalo", "desde", "hasta", "num_notas", "porcentaje"])
    notas  = datos["nota"].to_numpy(float)
    bordes = np.linspace(0, 10, intervalos + 1)
    conteos, _ = np.histogram(notas, bins=bordes)
    total = conteos.sum()
    return pd.DataFrame({
        "intervalo":  [f"{bordes[i]:.1f} - {bordes[i+1]:.1f}" for i in range(intervalos)],
        "desde":      bordes[:-1],
        "hasta":      bordes[1:],
        "num_notas":  conteos,
        "porcentaje": np.round(conteos / total * 100, 2) if total else conteos,
    })


# ---- 6. Formato ---- #

def formatear_nota(valor, decimales: int = 2) -> str:
    if valor is None or (isinstance(valor, float) and np.isnan(valor)):
        return "—"
    return f"{float(valor):.{decimales}f}"


def formatear_porcentaje(valor, decimales: int = 1) -> str:
    if valor is None or (isinstance(valor, float) and np.isnan(valor)):
        return "—"
    return f"{float(valor):.{decimales}f}%"


def preparar_tabla(tabla: pd.DataFrame) -> pd.DataFrame:
    vista = tabla.copy()
    for col in ("nota_media", "nota_maxima", "nota_minima"):
        if col in vista.columns:
            vista[col] = vista[col].astype(float).round(2)
    if "porcentaje_aprobados" in vista.columns:
        vista["porcentaje_aprobados"] = vista["porcentaje_aprobados"].astype(float).round(2)
    return vista
