# 🔍 Auditor de Datos Maestros de Proveedores

Aplicación web desarrollada con **Python + Streamlit** que valida los datos de nuevos proveedores antes de darlos de alta en el sistema, evitando errores manuales y duplicados.

---

## 📋 Descripción del proyecto

Esta herramienta automatiza tres comprobaciones clave del proceso de alta de proveedores:

1. **Validación de IBAN** — Comprueba el país, la longitud y los dígitos de control mediante el algoritmo módulo 97 (estándar ISO 13616).
2. **Validación de NIF / NIE / CIF** — Detecta el tipo de identificador y verifica su dígito o letra de control según la normativa española.
3. **Detección de duplicados** — Busca registros repetidos por NIF exacto, IBAN exacto o nombre comercial similar (usando similitud de cadenas).

---

## 🗂️ Estructura del proyecto

```
auditor_proveedores/
│
├── auditor_app.py      # Código principal: lógica de validación + interfaz Streamlit
└── README.md           # Este archivo
```

---

## ⚙️ Requisitos

- Python 3.9 o superior
- Las siguientes librerías (todas instalables con pip):

| Librería    | Uso                                              |
|-------------|--------------------------------------------------|
| `streamlit` | Interfaz web interactiva                         |
| `pandas`    | Lectura y manipulación de datos tabulares        |
| `openpyxl`  | Escritura del informe Excel con formato de color |

Instala todo con un solo comando:

```bash
pip install streamlit pandas openpyxl
```

---

## 🚀 Cómo ejecutar la aplicación

1. Abre una terminal en la carpeta del proyecto.
2. Ejecuta:

```bash
streamlit run auditor_app.py
```

3. El navegador se abrirá automáticamente en `http://localhost:8501`.

---

## 📥 Formato del archivo de entrada

La aplicación acepta archivos **Excel (.xlsx / .xls)** o **CSV (.csv)**.

El archivo debe contener al menos estas tres columnas (los nombres deben ser exactos):

| Columna  | Descripción                                    | Ejemplo                        |
|----------|------------------------------------------------|--------------------------------|
| `nombre` | Razón social o nombre comercial del proveedor  | `Suministros López S.L.`       |
| `nif`    | NIF, NIE o CIF del proveedor                   | `B12345674`                    |
| `iban`   | Número de cuenta bancaria en formato IBAN      | `ES9121000418450200051332`     |

> El archivo puede tener columnas adicionales; la aplicación solo audita las tres requeridas.

---

## 📤 Resultado de la auditoría

La app muestra:

- **Métricas resumen**: total de proveedores, válidos y a revisar.
- **Tabla interactiva**: cada fila en verde (✅ OK) o rojo (🔴 REVISAR) con el detalle del error.
- **Gráfico de barras**: distribución de los tipos de error encontrados.
- **Detalle expandible**: para cada proveedor con problemas, se despliegan los errores concretos.
- **Botón de descarga**: genera un informe en Excel con las mismas celdas coloreadas en verde y rojo.

---

## 🧪 Datos de prueba integrados

La aplicación incluye un conjunto de 6 proveedores de ejemplo que cubre todos los casos posibles. Pulsa el botón **"Cargar datos de prueba"** para usarlos sin necesidad de preparar ningún archivo.

| Proveedor              | NIF       | Resultado esperado                        |
|------------------------|-----------|-------------------------------------------|
| Suministros López S.L. | B12345674 | ✅ OK                                     |
| Suministros Lopez SL   | B12345674 | 🔴 NIF repetido + nombre similar          |
| Talleres Ruiz          | 12345678Z | 🔴 Dígitos de control del IBAN incorrectos|
| Electro Norte S.A.     | A58818501 | ✅ OK (el IBAN con espacios se normaliza)  |
| Limpiezas Sol          | 1234567X  | 🔴 Formato de NIF y IBAN incorrectos      |
| Gráficas Mar           | X1234567L | 🔴 IBAN de país no soportado (FR)         |

---

## 🧩 Organización del código

El archivo `auditor_app.py` está dividido en secciones claramente marcadas que siguen la estructura de trabajo semanal del proyecto:

| Sección              | Función principal          | Descripción                                              |
|----------------------|----------------------------|----------------------------------------------------------|
| Lunes (importación)  | `cargar_archivo()`         | Lee el Excel/CSV y valida que tenga las columnas necesarias |
| Martes (lógica)      | `validar_iban()`           | Algoritmo mod 97 para validar el IBAN                    |
|                      | `validar_nif()`            | Detecta DNI/NIE/CIF y verifica su dígito de control      |
|                      | `detectar_duplicados()`    | Cruza registros por NIF, IBAN y similitud de nombre      |
|                      | `auditar()`                | Orquesta todas las validaciones y construye el resultado  |
| Miércoles (salida)   | `exportar_excel()`         | Genera el Excel coloreado en memoria para su descarga    |
| Jueves/Viernes       | `main()`                   | Interfaz Streamlit: métricas, tabla, gráfico y descarga  |

---

## 🏫 Contexto académico

Proyecto de semana desarrollado en aproximadamente **22,5 horas** como ejercicio práctico de automatización de procesos administrativos con Python.

**Librerías estándar del curso utilizadas:**
- `pandas` — manipulación de datos tabulares
- `re` — expresiones regulares para validar formatos
- `unicodedata` / `difflib` — normalización y comparación de cadenas de texto
- `openpyxl` — generación de informes Excel con formato
- `streamlit` — interfaz web interactiva sin necesidad de HTML/CSS/JavaScript
