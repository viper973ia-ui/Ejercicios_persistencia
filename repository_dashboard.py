"""
repository.py
=============
Repositorio de datos y cálculos del Dashboard de Rendimiento Académico.

Este módulo concentra TODA la lógica de negocio: carga y limpieza de los CSV,
aplicación de filtros, cálculo de KPIs, estadísticas por asignatura, rendimiento
por alumno, evolución por evaluación, distribuciones y agrupaciones.

No contiene nada de interfaz (eso vive en ``app.py``) ni nada de dibujo
(eso vive en ``charts.py``), de modo que las funciones se pueden reutilizar
desde un notebook, un script o una API sin arrastrar Streamlit.

Dependencias: pandas, polars, numpy.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any, BinaryIO, Iterable, Sequence

import numpy as np
import pandas as pd
import polars as pl

# --------------------------------------------------------------------------- #
# Constantes del dominio
# --------------------------------------------------------------------------- #

RUTA_BASE: Path = Path(__file__).resolve().parent
ARCHIVO_ALUMNOS: Path = RUTA_BASE / "Alumnos.csv"
ARCHIVO_NOTAS: Path = RUTA_BASE / "Notas.csv"

NOTA_APROBADO: float = 5.0
NOTA_MAXIMA: float = 10.0
NOTA_MINIMA: float = 0.0
GRUPO_DESCONOCIDO: str = "Sin grupo"
TODOS: str = "Todos"

COLUMNAS_ESTADISTICAS_ASIGNATURA: list[str] = [
    "asignatura",
    "alumnos_evaluados",
    "nota_media",
    "nota_maxima",
    "nota_minima",
    "porcentaje_aprobados",
]

COLUMNAS_RENDIMIENTO_ALUMNO: list[str] = [
    "id_alumno",
    "nombre",
    "curso",
    "grupo",
    "nota_media",
    "asignaturas_evaluadas",
    "asignaturas_aprobadas",
]


# --------------------------------------------------------------------------- #
# 1. Carga y limpieza de datos
# --------------------------------------------------------------------------- #

def _leer_csv(origen: str | Path | BinaryIO) -> pd.DataFrame:
    """Lee un CSV desde una ruta del disco o desde un fichero en memoria.

    Parameters
    ----------
    origen:
        Ruta (``str``/``Path``) o fichero binario tipo ``st.file_uploader``.
    """
    if isinstance(origen, (str, Path)):
        return pd.read_csv(origen)
    return pd.read_csv(origen)


def cargar_alumnos(origen: str | Path | BinaryIO | None = None) -> pd.DataFrame:
    """Carga y normaliza el catálogo de alumnos.

    Limpieza aplicada:
      * ``grupo`` vacío -> ``"Sin grupo"``.
      * ``nombre`` sin espacios sobrantes y en formato título.
      * ``edad`` numérica (nulos -> ``NaN``).
      * ``id_alumno`` como entero.

    Returns
    -------
    pandas.DataFrame
        Columnas: ``id_alumno, nombre, edad, curso, grupo``.
    """
    df = _leer_csv(origen if origen is not None else ARCHIVO_ALUMNOS)

    df["id_alumno"] = pd.to_numeric(df["id_alumno"], errors="coerce").astype("Int64")
    df["nombre"] = df["nombre"].astype(str).str.strip().str.title()
    df["edad"] = pd.to_numeric(df["edad"], errors="coerce").astype("Int64")
    df["curso"] = df["curso"].astype(str).str.strip()
    df["grupo"] = (
        df["grupo"]
        .astype("string")
        .str.strip()
        .replace({"": pd.NA, "nan": pd.NA, "None": pd.NA})
        .fillna(GRUPO_DESCONOCIDO)
    )

    return df.dropna(subset=["id_alumno"]).reset_index(drop=True)


def cargar_notas(origen: str | Path | BinaryIO | None = None) -> pd.DataFrame:
    """Carga y valida las calificaciones.

    Limpieza aplicada:
      * ``nota`` numérica y acotada al rango [0, 10].
      * ``evaluacion`` como entero.
      * Se descartan filas sin ``id_alumno`` o sin ``nota``.

    Returns
    -------
    pandas.DataFrame
        Columnas: ``id_nota, id_alumno, asignatura, evaluacion, nota``.
    """
    df = _leer_csv(origen if origen is not None else ARCHIVO_NOTAS)

    df["id_alumno"] = pd.to_numeric(df["id_alumno"], errors="coerce").astype("Int64")
    df["evaluacion"] = pd.to_numeric(df["evaluacion"], errors="coerce").astype("Int64")
    df["nota"] = pd.to_numeric(df["nota"], errors="coerce")
    df["asignatura"] = df["asignatura"].astype(str).str.strip()

    df = df.dropna(subset=["id_alumno", "nota"])
    df["nota"] = df["nota"].clip(lower=NOTA_MINIMA, upper=NOTA_MAXIMA)

    return df.reset_index(drop=True)


def construir_dataset(
    alumnos: pd.DataFrame,
    notas: pd.DataFrame,
) -> pd.DataFrame:
    """Une alumnos y notas en una única tabla analítica (grano: una nota).

    Añade las columnas derivadas ``aprobado`` (nota >= 5) y ``curso``/``grupo``
    del alumno. Las notas de alumnos no presentes en el catálogo se conservan
    con nombre ``"Desconocido"`` para no perder información.
    """
    datos = notas.merge(
        alumnos,
        on="id_alumno",
        how="left",
        validate="many_to_one",
    )

    datos["nombre"] = datos["nombre"].fillna("Desconocido")
    datos["curso"] = datos["curso"].fillna("Sin curso")
    datos["grupo"] = datos["grupo"].fillna(GRUPO_DESCONOCIDO)
    datos["aprobado"] = datos["nota"] >= NOTA_APROBADO

    columnas = [
        "id_nota",
        "id_alumno",
        "nombre",
        "edad",
        "curso",
        "grupo",
        "asignatura",
        "evaluacion",
        "nota",
        "aprobado",
    ]
    return datos[[c for c in columnas if c in datos.columns]].reset_index(drop=True)


def cargar_datos(
    archivo_alumnos: str | Path | BinaryIO | None = None,
    archivo_notas: str | Path | BinaryIO | None = None,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Punto de entrada único: devuelve ``(alumnos, notas, dataset)``."""
    alumnos = cargar_alumnos(archivo_alumnos)
    notas = cargar_notas(archivo_notas)
    return alumnos, notas, construir_dataset(alumnos, notas)


# --------------------------------------------------------------------------- #
# 2. Filtros
# --------------------------------------------------------------------------- #

def obtener_opciones(datos: pd.DataFrame) -> dict[str, list[Any]]:
    """Devuelve los valores únicos ordenados de cada filtro de la barra lateral."""
    if datos.empty:
        return {"curso": [], "asignatura": [], "grupo": [], "evaluacion": []}

    return {
        "curso": sorted(datos["curso"].dropna().unique().tolist()),
        "asignatura": sorted(datos["asignatura"].dropna().unique().tolist()),
        "grupo": sorted(datos["grupo"].dropna().unique().tolist()),
        "evaluacion": sorted(datos["evaluacion"].dropna().unique().tolist()),
    }


def aplicar_filtros(
    datos: pd.DataFrame,
    curso: str | None = None,
    asignatura: str | None = None,
    grupo: str | None = None,
    evaluacion: int | str | None = None,
) -> pd.DataFrame:
    """Filtra el dataset por curso, asignatura, grupo y evaluación.

    Un valor ``None``, ``"Todos"`` o una lista vacía significa "sin filtrar".
    """
    filtrado = datos

    def _es_todos(valor: Any) -> bool:
        return valor is None or valor == TODOS or valor == [] or valor == ""

    if not _es_todos(curso):
        filtrado = filtrado[filtrado["curso"] == curso]
    if not _es_todos(asignatura):
        filtrado = filtrado[filtrado["asignatura"] == asignatura]
    if not _es_todos(grupo):
        filtrado = filtrado[filtrado["grupo"] == grupo]
    if not _es_todos(evaluacion):
        filtrado = filtrado[filtrado["evaluacion"] == evaluacion]

    return filtrado.reset_index(drop=True)


# --------------------------------------------------------------------------- #
# 3. KPIs
# --------------------------------------------------------------------------- #

def calcular_kpis(datos: pd.DataFrame) -> dict[str, float | int]:
    """Calcula los indicadores principales que se muestran en las tarjetas.

    Returns
    -------
    dict
        ``alumnos_evaluados``, ``nota_media``, ``nota_maxima``, ``nota_minima``,
        ``porcentaje_aprobados``, ``num_notas``, ``num_asignaturas``.
    """
    vacio: dict[str, float | int] = {
        "alumnos_evaluados": 0,
        "nota_media": 0.0,
        "nota_maxima": 0.0,
        "nota_minima": 0.0,
        "porcentaje_aprobados": 0.0,
        "num_notas": 0,
        "num_asignaturas": 0,
    }
    if datos.empty:
        return vacio

    notas = datos["nota"].to_numpy(dtype=float)
    aprobados = datos["aprobado"].to_numpy(dtype=bool)

    return {
        "alumnos_evaluados": int(datos["id_alumno"].nunique()),
        "nota_media": float(np.mean(notas)),
        "nota_maxima": float(np.max(notas)),
        "nota_minima": float(np.min(notas)),
        "porcentaje_aprobados": float(np.mean(aprobados) * 100.0),
        "num_notas": int(notas.size),
        "num_asignaturas": int(datos["asignatura"].nunique()),
    }


# --------------------------------------------------------------------------- #
# 4. Estadísticas agregadas
# --------------------------------------------------------------------------- #

def _a_polars(datos: pd.DataFrame) -> pl.DataFrame:
    """Convierte el DataFrame de pandas a polars para las agregaciones.

    Se construye columna a columna con NumPy para no depender de pyarrow
    (dependencia opcional de polars) y para conservar los enteros como enteros.
    """
    columnas: dict[str, Any] = {}
    for nombre in datos.columns:
        serie = datos[nombre]
        if pd.api.types.is_bool_dtype(serie):
            columnas[nombre] = serie.to_numpy(dtype=bool)
        elif pd.api.types.is_integer_dtype(serie):
            if serie.isna().any():
                columnas[nombre] = serie.astype("float64").to_numpy()
            else:
                columnas[nombre] = serie.astype("int64").to_numpy()
        elif pd.api.types.is_float_dtype(serie):
            columnas[nombre] = serie.to_numpy(dtype="float64")
        else:
            columnas[nombre] = serie.astype(str).to_numpy()
    return pl.DataFrame(columnas)


def _a_pandas(marco: pl.DataFrame) -> pd.DataFrame:
    """Convierte un DataFrame de polars a pandas sin pasar por pyarrow."""
    return pd.DataFrame(marco.to_dict(as_series=False))


def estadisticas_por_asignatura(datos: pd.DataFrame) -> pd.DataFrame:
    """Resumen por asignatura: alumnos, media, máximo, mínimo y % de aprobados.

    Returns
    -------
    pandas.DataFrame
        Columnas de ``COLUMNAS_ESTADISTICAS_ASIGNATURA`` ordenadas por media
        descendente.
    """
    if datos.empty:
        return pd.DataFrame(columns=COLUMNAS_ESTADISTICAS_ASIGNATURA)

    resultado = (
        _a_polars(datos)
        .group_by("asignatura")
        .agg(
            pl.col("id_alumno").n_unique().alias("alumnos_evaluados"),
            pl.col("nota").mean().alias("nota_media"),
            pl.col("nota").max().alias("nota_maxima"),
            pl.col("nota").min().alias("nota_minima"),
            (pl.col("aprobado").mean() * 100.0).alias("porcentaje_aprobados"),
        )
        .sort("nota_media", descending=True)
    )
    resultado = _a_pandas(resultado)

    return resultado[COLUMNAS_ESTADISTICAS_ASIGNATURA]


def rendimiento_por_alumno(datos: pd.DataFrame) -> pd.DataFrame:
    """Rendimiento individual: media, asignaturas evaluadas y aprobadas.

    Una asignatura se considera aprobada cuando la media del alumno en esa
    asignatura alcanza ``NOTA_APROBADO``.

    Returns
    -------
    pandas.DataFrame
        Columnas de ``COLUMNAS_RENDIMIENTO_ALUMNO`` ordenadas por media
        descendente.
    """
    if datos.empty:
        return pd.DataFrame(columns=COLUMNAS_RENDIMIENTO_ALUMNO)

    marco = _a_polars(datos)

    por_asignatura = marco.group_by(["id_alumno", "asignatura"]).agg(
        pl.col("nota").mean().alias("media_asignatura")
    )

    resumen = por_asignatura.group_by("id_alumno").agg(
        pl.col("asignatura").n_unique().alias("asignaturas_evaluadas"),
        (pl.col("media_asignatura") >= NOTA_APROBADO)
        .sum()
        .alias("asignaturas_aprobadas"),
        pl.col("media_asignatura").mean().alias("nota_media"),
    )

    identidad = marco.group_by(["id_alumno", "nombre", "curso", "grupo"]).agg(
        pl.len().alias("num_notas")
    )

    resultado = (
        identidad.join(resumen, on="id_alumno", how="left")
        .sort("nota_media", descending=True)
    )
    resultado = _a_pandas(resultado)

    return resultado[COLUMNAS_RENDIMIENTO_ALUMNO]


def evolucion_por_evaluacion(datos: pd.DataFrame) -> pd.DataFrame:
    """Nota media global por evaluación.

    Returns
    -------
    pandas.DataFrame
        Columnas: ``evaluacion, nota_media, nota_maxima, nota_minima,
        porcentaje_aprobados, num_notas``.
    """
    columnas = [
        "evaluacion",
        "nota_media",
        "nota_maxima",
        "nota_minima",
        "porcentaje_aprobados",
        "num_notas",
    ]
    if datos.empty:
        return pd.DataFrame(columns=columnas)

    resultado = (
        _a_polars(datos)
        .group_by("evaluacion")
        .agg(
            pl.col("nota").mean().alias("nota_media"),
            pl.col("nota").max().alias("nota_maxima"),
            pl.col("nota").min().alias("nota_minima"),
            (pl.col("aprobado").mean() * 100.0).alias("porcentaje_aprobados"),
            pl.len().alias("num_notas"),
        )
        .sort("evaluacion")
    )
    resultado = _a_pandas(resultado)

    return resultado[columnas]


def evolucion_por_asignatura(datos: pd.DataFrame) -> pd.DataFrame:
    """Nota media por evaluación y asignatura (para el gráfico de líneas).

    Returns
    -------
    pandas.DataFrame
        Columnas: ``evaluacion, asignatura, nota_media, num_notas``.
    """
    columnas = ["evaluacion", "asignatura", "nota_media", "num_notas"]
    if datos.empty:
        return pd.DataFrame(columns=columnas)

    resultado = (
        _a_polars(datos)
        .group_by(["evaluacion", "asignatura"])
        .agg(
            pl.col("nota").mean().alias("nota_media"),
            pl.len().alias("num_notas"),
        )
        .sort(["asignatura", "evaluacion"])
    )
    resultado = _a_pandas(resultado)

    return resultado[columnas]


def estadisticas_por_grupo(datos: pd.DataFrame) -> pd.DataFrame:
    """Resumen por grupo (A, B, ...): alumnos, media y % de aprobados."""
    columnas = ["grupo", "alumnos", "nota_media", "porcentaje_aprobados"]
    if datos.empty:
        return pd.DataFrame(columns=columnas)

    resultado = (
        _a_polars(datos)
        .group_by("grupo")
        .agg(
            pl.col("id_alumno").n_unique().alias("alumnos"),
            pl.col("nota").mean().alias("nota_media"),
            (pl.col("aprobado").mean() * 100.0).alias("porcentaje_aprobados"),
        )
        .sort("grupo")
    )
    resultado = _a_pandas(resultado)

    return resultado[columnas]


def estadisticas_por_curso(datos: pd.DataFrame) -> pd.DataFrame:
    """Resumen por curso (Python, Java, ...): alumnos, media y % de aprobados."""
    columnas = ["curso", "alumnos", "nota_media", "porcentaje_aprobados"]
    if datos.empty:
        return pd.DataFrame(columns=columnas)

    resultado = (
        _a_polars(datos)
        .group_by("curso")
        .agg(
            pl.col("id_alumno").n_unique().alias("alumnos"),
            pl.col("nota").mean().alias("nota_media"),
            (pl.col("aprobado").mean() * 100.0).alias("porcentaje_aprobados"),
        )
        .sort("nota_media", descending=True)
    )
    resultado = _a_pandas(resultado)

    return resultado[columnas]


# --------------------------------------------------------------------------- #
# 5. Distribución de notas
# --------------------------------------------------------------------------- #

def resumen_distribucion(datos: pd.DataFrame) -> dict[str, float]:
    """Estadísticos descriptivos de las notas (media, mediana, desviación...)."""
    if datos.empty:
        return {
            "media": 0.0,
            "mediana": 0.0,
            "desviacion": 0.0,
            "p25": 0.0,
            "p75": 0.0,
            "minimo": 0.0,
            "maximo": 0.0,
        }

    notas = datos["nota"].to_numpy(dtype=float)
    return {
        "media": float(np.mean(notas)),
        "mediana": float(np.median(notas)),
        "desviacion": float(np.std(notas, ddof=1)) if notas.size > 1 else 0.0,
        "p25": float(np.percentile(notas, 25)),
        "p75": float(np.percentile(notas, 75)),
        "minimo": float(np.min(notas)),
        "maximo": float(np.max(notas)),
    }


def tabla_distribucion(
    datos: pd.DataFrame,
    intervalos: int = 10,
) -> pd.DataFrame:
    """Cuenta notas por intervalo (histograma en forma de tabla).

    Parameters
    ----------
    intervalos:
        Número de tramos entre 0 y 10.

    Returns
    -------
    pandas.DataFrame
        Columnas: ``intervalo, desde, hasta, num_notas, porcentaje``.
    """
    columnas = ["intervalo", "desde", "hasta", "num_notas", "porcentaje"]
    if datos.empty:
        return pd.DataFrame(columns=columnas)

    notas = datos["nota"].to_numpy(dtype=float)
    bordes = np.linspace(NOTA_MINIMA, NOTA_MAXIMA, intervalos + 1)
    conteos, _ = np.histogram(notas, bins=bordes)
    total = conteos.sum()

    return pd.DataFrame(
        {
            "intervalo": [
                f"{bordes[i]:.1f} - {bordes[i + 1]:.1f}" for i in range(intervalos)
            ],
            "desde": bordes[:-1],
            "hasta": bordes[1:],
            "num_notas": conteos,
            "porcentaje": np.round(conteos / total * 100.0, 2) if total else conteos,
        }
    )


def conteo_por_estado(datos: pd.DataFrame) -> pd.DataFrame:
    """Número de notas aprobadas y suspensas (para el gráfico circular)."""
    columnas = ["estado", "num_notas"]
    if datos.empty:
        return pd.DataFrame(columns=columnas)

    resultado = (
        _a_polars(datos)
        .group_by("aprobado")
        .agg(pl.len().alias("num_notas"))
        .sort("aprobado")
    )
    resultado = _a_pandas(resultado)
    resultado["estado"] = resultado["aprobado"].map(
        {True: "Aprobado", False: "Suspenso"}
    )
    return resultado[["estado", "num_notas"]]


def ranking_alumnos(datos: pd.DataFrame, limite: int = 10) -> pd.DataFrame:
    """Devuelve los ``limite`` alumnos con mejor nota media."""
    return rendimiento_por_alumno(datos).head(limite).reset_index(drop=True)


# --------------------------------------------------------------------------- #
# 6. Utilidades de formato y exportación
# --------------------------------------------------------------------------- #

def formatear_nota(valor: float | int | None, decimales: int = 2) -> str:
    """Formatea una nota con el número de decimales indicado."""
    if valor is None or (isinstance(valor, float) and np.isnan(valor)):
        return "—"
    return f"{float(valor):.{decimales}f}"


def formatear_porcentaje(valor: float | int | None, decimales: int = 1) -> str:
    """Formatea un porcentaje ya expresado en base 100."""
    if valor is None or (isinstance(valor, float) and np.isnan(valor)):
        return "—"
    return f"{float(valor):.{decimales}f}%"


def preparar_tabla_para_mostrar(
    tabla: pd.DataFrame,
    columnas_nota: Sequence[str] = ("nota_media", "nota_maxima", "nota_minima"),
    columnas_porcentaje: Sequence[str] = ("porcentaje_aprobados",),
) -> pd.DataFrame:
    """Redondea las columnas numéricas para presentarlas en pantalla."""
    vista = tabla.copy()
    for columna in columnas_nota:
        if columna in vista.columns:
            vista[columna] = vista[columna].astype(float).round(2)
    for columna in columnas_porcentaje:
        if columna in vista.columns:
            vista[columna] = vista[columna].astype(float).round(2)
    return vista


def exportar_csv(datos: pd.DataFrame) -> bytes:
    """Serializa un DataFrame a CSV (UTF-8) para el botón de descarga."""
    return datos.to_csv(index=False).encode("utf-8")


def listar_asignaturas(datos: pd.DataFrame) -> list[str]:
    """Lista ordenada de asignaturas presentes en el dataset."""
    if datos.empty:
        return []
    return sorted(datos["asignatura"].dropna().unique().tolist())


def filtrar_por_asignaturas(
    datos: pd.DataFrame,
    asignaturas: Iterable[str],
) -> pd.DataFrame:
    """Filtra el dataset por una colección de asignaturas."""
    seleccion = list(asignaturas)
    if not seleccion:
        return datos
    return datos[datos["asignatura"].isin(seleccion)].reset_index(drop=True)
