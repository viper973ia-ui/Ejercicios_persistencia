"""
Auditor de Datos Maestros de Proveedores — Streamlit
Valida IBAN, NIF/NIE/CIF y detecta duplicados antes de dar de alta proveedores.
"""

import io
import re
import unicodedata
from difflib import SequenceMatcher

import pandas as pd
import streamlit as st
from openpyxl import load_workbook
from openpyxl.styles import Font, PatternFill

# ─── Constantes ────────────────────────────────────────────────────────────────
TOLERANCIA_SIMILITUD = 0.88
LETRAS_DNI = "TRWAGMYFPDXBNJZSQVHLCKE"
LONGITUD_IBAN = {
    "ES": 24, "PT": 25, "FR": 27, "DE": 22,
    "IT": 27, "GB": 22, "NL": 18, "BE": 16,
}
COLUMNAS = {"nombre", "nif", "iban"}


# ─── Lógica de validación ───────────────────────────────────────────────────────
def limpiar_texto(valor):
    """Quita espacios y pasa a mayúsculas; devuelve '' si es nulo."""
    return "" if pd.isna(valor) else re.sub(r"\s+", "", str(valor)).upper()


def validar_iban(iban):
    iban = limpiar_texto(iban)
    if not re.fullmatch(r"[A-Z]{2}\d{2}[A-Z0-9]+", iban):
        return "IBAN con formato incorrecto"
    pais = iban[:2]
    if pais not in LONGITUD_IBAN:
        return f"País {pais} no soportado"
    if len(iban) != LONGITUD_IBAN[pais]:
        return f"Longitud incorrecta para {pais} (esperada {LONGITUD_IBAN[pais]})"
    reordenado = iban[4:] + iban[:4]
    numerico = "".join(str(int(c, 36)) for c in reordenado)
    return "" if int(numerico) % 97 == 1 else "Dígitos de control del IBAN incorrectos"


def validar_dni_nie(nif):
    if nif[0] in "XYZ":
        nif = str("XYZ".index(nif[0])) + nif[1:]
    return nif[8] == LETRAS_DNI[int(nif[:8]) % 23]


def validar_cif(cif):
    digitos = [int(c) for c in cif[1:8]]
    pares = sum(digitos[1::2])
    impares = sum(sum(divmod(d * 2, 10)) for d in digitos[0::2])
    control = (10 - (pares + impares) % 10) % 10
    if cif[0] in "PQRSNW":
        return cif[8] == "JABCDEFGHI"[control]
    if cif[0] in "ABEH":
        return cif[8] == str(control)
    return cif[8] in (str(control), "JABCDEFGHI"[control])


def validar_nif(nif):
    nif = limpiar_texto(nif)
    if not nif:
        return "NIF vacío"
    if re.fullmatch(r"\d{8}[A-Z]|[XYZ]\d{7}[A-Z]", nif):
        return "" if validar_dni_nie(nif) else "Letra del DNI/NIE incorrecta"
    if re.fullmatch(r"[ABCDEFGHJNPQRSUVW]\d{7}[0-9A-J]", nif):
        return "" if validar_cif(nif) else "Dígito de control del CIF incorrecto"
    return "Formato de NIF/CIF no válido"


def normalizar_nombre(nombre):
    texto = unicodedata.normalize("NFD", str(nombre).lower())
    texto = "".join(c for c in texto if unicodedata.category(c) != "Mn")
    texto = re.sub(r"\b(s\.?l\.?u?|s\.?a\.?|s\.?l\.?l\.?)\b", "", texto)
    return re.sub(r"[^a-z0-9 ]", "", texto).strip()


def detectar_duplicados(df):
    duplicados = {}
    nombres = df["nombre"].map(normalizar_nombre).tolist()
    nifs = df["nif"].map(limpiar_texto).tolist()
    ibans = df["iban"].map(limpiar_texto).tolist()
    for i in range(len(df)):
        for j in range(i):
            if nifs[i] and nifs[i] == nifs[j]:
                duplicados[i] = f"NIF repetido (fila {j + 2})"
            elif ibans[i] and ibans[i] == ibans[j]:
                duplicados[i] = f"IBAN repetido (fila {j + 2})"
            elif SequenceMatcher(None, nombres[i], nombres[j]).ratio() >= TOLERANCIA_SIMILITUD:
                duplicados[i] = f"Nombre similar a fila {j + 2}"
            if i in duplicados:
                break
    return duplicados


def auditar(df):
    df = df.copy()
    dups = detectar_duplicados(df)
    errores = []
    for i, fila in df.iterrows():
        problemas = [p for p in (
            validar_nif(fila["nif"]),
            validar_iban(fila["iban"]),
            dups.get(i, ""),
        ) if p]
        errores.append("; ".join(problemas))
    df["errores"] = errores
    df["estado"] = ["✅ OK" if not e else "🔴 REVISAR" for e in errores]
    return df


# ─── Exportar a Excel coloreado ─────────────────────────────────────────────────
def exportar_excel(df):
    buffer = io.BytesIO()
    df.to_excel(buffer, index=False, sheet_name="Auditoría", engine="openpyxl")
    buffer.seek(0)
    wb = load_workbook(buffer)
    ws = wb.active
    rojo = PatternFill("solid", start_color="FFC7CE")
    verde = PatternFill("solid", start_color="C6EFCE")
    idx_estado = next(c.column for c in ws[1] if c.value == "estado")
    for c in ws[1]:
        c.font = Font(bold=True)
    for fila in ws.iter_rows(min_row=2):
        color = verde if "OK" in str(fila[idx_estado - 1].value) else rojo
        for celda in fila:
            celda.fill = color
    for col in ws.columns:
        ws.column_dimensions[col[0].column_letter].width = 32
    out = io.BytesIO()
    wb.save(out)
    out.seek(0)
    return out


# ─── Datos de prueba ────────────────────────────────────────────────────────────
def datos_prueba():
    return pd.DataFrame({
        "nombre":  ["Suministros López S.L.", "Suministros Lopez SL",
                    "Talleres Ruiz", "Electro Norte S.A.",
                    "Limpiezas Sol", "Gráficas Mar"],
        "nif":     ["B12345674", "B12345674", "12345678Z",
                    "A58818501", "1234567X", "X1234567L"],
        "iban":    ["ES9121000418450200051332", "ES9121000418450200051332",
                    "ES9121000418450200051333", "ES91 2100 0418 4502 0005 1332",
                    "ES12", "FR1420041010050500013M02606"],
    })


# ─── Interfaz Streamlit ─────────────────────────────────────────────────────────
def main():
    st.set_page_config(
        page_title="Auditor de Proveedores",
        page_icon="🔍",
        layout="wide",
    )

    # Cabecera
    st.title("🔍 Auditor de Datos Maestros de Proveedores")
    st.markdown(
        "Valida **IBAN**, **NIF / NIE / CIF** y detecta posibles **duplicados** "
        "antes de dar de alta a un proveedor en el sistema."
    )
    st.divider()

    # Columnas de carga
    col_izq, col_der = st.columns([1, 1], gap="large")

    with col_izq:
        st.subheader("📂 Cargar archivo")
        archivo = st.file_uploader(
            "Sube un Excel o CSV con columnas: **nombre**, **nif**, **iban**",
            type=["xlsx", "xls", "csv"],
        )
        st.caption("El archivo puede tener más columnas; solo se auditan las tres requeridas.")

    with col_der:
        st.subheader("🧪 O bien, usa los datos de prueba")
        st.markdown(
            "Incluye 6 proveedores con casos variados: "
            "NIF duplicado, IBAN incorrecto, nombre similar y registros válidos."
        )
        usar_prueba = st.button("Cargar datos de prueba", use_container_width=True)

    st.divider()

    # Determinar fuente de datos
    df_entrada = None

    if usar_prueba:
        df_entrada = datos_prueba()
        st.info("Usando los datos de prueba integrados.")

    elif archivo is not None:
        try:
            if archivo.name.endswith(".csv"):
                df_entrada = pd.read_csv(archivo)
            else:
                df_entrada = pd.read_excel(archivo)

            faltan = COLUMNAS - set(df_entrada.columns)
            if faltan:
                st.error(f"❌ Faltan columnas obligatorias: **{', '.join(sorted(faltan))}**")
                df_entrada = None
            elif df_entrada.empty:
                st.error("❌ El archivo está vacío.")
                df_entrada = None
        except Exception as e:
            st.error(f"❌ Error al leer el archivo: {e}")

    # Auditoría y resultados
    if df_entrada is not None:
        with st.spinner("Auditando proveedores…"):
            df_resultado = auditar(df_entrada)

        # Métricas
        total = len(df_resultado)
        ok = (df_resultado["estado"] == "✅ OK").sum()
        revisar = total - ok
        tipos_error = {}
        for err in df_resultado["errores"]:
            for parte in err.split(";"):
                parte = parte.strip()
                if parte:
                    clave = parte.split("(")[0].strip()
                    tipos_error[clave] = tipos_error.get(clave, 0) + 1

        m1, m2, m3 = st.columns(3)
        m1.metric("Total proveedores", total)
        m2.metric("✅ Válidos", ok)
        m3.metric("🔴 A revisar", revisar, delta=f"-{revisar}" if revisar else None,
                  delta_color="inverse")

        st.divider()

        # Tabla con estilo condicional
        st.subheader("📋 Resultado de la auditoría")

        def colorear_fila(fila):
            color = "#c6efce" if "OK" in fila["estado"] else "#ffc7ce"
            return [f"background-color: {color}"] * len(fila)

        columnas_visibles = [c for c in df_resultado.columns
                             if c not in {"nif", "iban", "nombre"}]
        columnas_orden = ["nombre", "nif", "iban", "estado", "errores"]
        columnas_orden = [c for c in columnas_orden if c in df_resultado.columns]

        st.dataframe(
            df_resultado[columnas_orden].style.apply(colorear_fila, axis=1),
            use_container_width=True,
            height=min(80 + total * 38, 520),
        )

        # Desglose de errores
        if tipos_error:
            st.divider()
            st.subheader("📊 Tipos de error encontrados")
            df_errores = (pd.DataFrame.from_dict(tipos_error, orient="index", columns=["Registros"])
                          .sort_values("Registros", ascending=False))
            st.bar_chart(df_errores)

        # Detalle por proveedor problemático
        if revisar:
            st.divider()
            st.subheader("🔎 Detalle de proveedores a revisar")
            df_revisar = df_resultado[df_resultado["estado"] != "✅ OK"].reset_index(drop=True)
            for _, fila in df_revisar.iterrows():
                with st.expander(f"🔴 {fila['nombre']}  —  NIF: {fila['nif']}"):
                    col1, col2 = st.columns(2)
                    col1.markdown(f"**IBAN:** `{fila['iban']}`")
                    col2.markdown(f"**NIF:** `{fila['nif']}`")
                    for err in fila["errores"].split(";"):
                        if err.strip():
                            st.error(f"⚠️ {err.strip()}")

        # Descarga
        st.divider()
        excel_bytes = exportar_excel(df_resultado)
        st.download_button(
            label="⬇️ Descargar informe en Excel",
            data=excel_bytes,
            file_name="auditoria_proveedores.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True,
            type="primary",
        )

    else:
        st.markdown(
            "<div style='text-align:center;color:#888;padding:60px 0'>"
            "Sube un archivo o carga los datos de prueba para comenzar la auditoría."
            "</div>",
            unsafe_allow_html=True,
        )


if __name__ == "__main__":
    main()
