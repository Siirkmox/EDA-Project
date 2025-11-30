# 📊 Análisis de la Inversión en I+D en España (2000-2024)

Análisis Exploratorio de Datos (EDA) sobre la evolución de la inversión en Investigación y Desarrollo en España durante el período 2000-2024.

## 🎯 Objetivos del Proyecto

Este proyecto analiza la evolución temporal del gasto en I+D en España para:

1. **Evolución temporal** del gasto total en I+D (2000-2024)
2. **Distribución sectorial** del gasto entre sectores ejecutores
3. **Análisis del origen** de los fondos que financian la I+D
4. **Impacto de eventos económicos** (Crisis Financiera 2008, Pandemia COVID-19)
5. **Identificación de tendencias** y patrones en la inversión en innovación

## 📁 Estructura del Proyecto

```
EDA-Project/
├── data/
│   ├── original/                      # Datos originales del INE
│   │   ├── gastoI+D1964-2021.csv
│   │   ├── gastoI+D2021-2024.csv
│   │   ├── origenfondosI+D1964-2021.csv
│   │   └── origenfondosI+D2021-2024.csv
│   ├── consolidatedDataset/           # Datos consolidados (4→2 archivos)
│   │   ├── gastos_consolidados.csv
│   │   └── fondos_consolidados.csv
│   └── cleanedDataset/                # Datos limpios y procesados
│       ├── gastos_clean.csv
│       └── fondos_clean.csv
├── notebooks/
│   ├── exploration.ipynb              # Notebook 1: Exploración inicial
│   ├── transformation.ipynb           # Notebook 2: Limpieza y transformación
│   └── eda.ipynb                      # Notebook 3: Análisis y visualizaciones
├── src/
│   ├── __init__.py
│   ├── cleaning.py                    # Funciones de limpieza de datos
│   └── visualization.py               # Funciones de visualización
└── README.md
```

## 🚀 Flujo de Trabajo

El proyecto sigue un pipeline modular de análisis de datos:

### 1️⃣ Exploración (`exploration.ipynb`)
- Carga de 4 datasets originales del INE
- Consolidación en 2 datasets (gastos y fondos)
- Eliminación de duplicados (año 2021)
- Filtrado al período 2000-2024
- Análisis de calidad de datos

**Output:** `gastos_consolidados.csv`, `fondos_consolidados.csv`

### 2️⃣ Transformación (`transformation.ipynb`)
- Limpieza de formato numérico europeo
- Tratamiento de valores faltantes
- Separación de valores absolutos y porcentajes
- Transformación de formato largo a ancho (pivot)
- Renombrado de columnas
- Uso de funciones modulares de `src/cleaning.py`

**Output:** `gastos_clean.csv`, `fondos_clean.csv`

### 3️⃣ Análisis EDA (`eda.ipynb`)
- Visualización de evolución temporal
- Análisis de distribución sectorial
- Análisis del origen de fondos
- Impacto de eventos económicos
- Histogramas de distribución del gasto total y crecimiento interanual
- Conclusiones y hallazgos
- Uso de funciones modulares de `src/visualization.py`

**Output:** Visualizaciones y análisis

## 📊 Fuente de Datos

**Instituto Nacional de Estadística (INE)**
- [Gastos I+D 2021-2024](https://www.ine.es/jaxi/Tabla.htm?tpx=76743&L=0)
- [Gastos I+D 1964-2021](https://www.ine.es/jaxi/Tabla.htm?tpx=76787&L=0)
- [Fondos I+D 2021-2024](https://www.ine.es/jaxi/Tabla.htm?tpx=76745&L=0)
- [Fondos I+D 1964-2021](https://www.ine.es/jaxi/Tabla.htm?tpx=76789&L=0)

## 🛠️ Requisitos

### Librerías Python

```bash
pip install pandas numpy matplotlib seaborn
```

O usar el archivo de requisitos:

```bash
pip install -r requirements.txt
```

### Versiones recomendadas
- Python 3.8+
- pandas >= 1.3.0
- numpy >= 1.21.0
- matplotlib >= 3.4.0
- seaborn >= 0.11.0

## 📖 Cómo Usar Este Proyecto

### Opción 1: Ejecutar todos los notebooks en orden

```bash
# 1. Clonar o descargar el repositorio
cd EDA-Project

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Ejecutar notebooks en orden
jupyter notebook notebooks/exploration.ipynb
jupyter notebook notebooks/transformation.ipynb
jupyter notebook notebooks/eda.ipynb
```

### Opción 2: Usar las funciones modulares

```python
import sys
sys.path.append('src/')
from cleaning import limpiar_columna_total, pivotear_dataset
from visualization import plot_evolucion_temporal

# Cargar datos
import pandas as pd
df = pd.read_csv('data/cleanedDataset/gastos_clean.csv', index_col='Años')

# Generar visualización
plot_evolucion_temporal(df)
```

## 📈 Principales Hallazgos

### Evolución del Gasto
- **Crecimiento del >300%** en el período 2000-2024
- Inversión de **5.7 mil millones de €** en 2000 → **24 mil millones de €** en 2024
- Máximo histórico alcanzado en 2024

### Impacto de Crisis Económicas
- **Crisis 2008**: Descenso del ~10% entre 2008-2013 (5 años de recesión)
- **COVID-19**: Sin caída significativa, recuperación rápida en 2021 (+8-10%)
- Mayor resiliencia ante crisis sanitarias vs. crisis financieras

### Distribución Sectorial
- **Empresas**: 56% del gasto total (principal ejecutor)
- **Enseñanza Superior**: 25% (universidades e investigación académica)
- **Administración Pública**: 18%
- **IPSFL**: 0.3% (organizaciones sin ánimo de lucro)

### Origen de Fondos
- **Empresas**: 48% de la financiación
- **Administración Pública**: 43%
- **Resto del Mundo**: 9% (financiación internacional)
- Balance equilibrado público-privado

## 🔧 Módulos Principales

### `src/cleaning.py`
Funciones para limpieza y transformación de datos:
- `limpiar_columna_total()`: Convierte formato europeo a numérico
- `separar_valores_porcentajes()`: Separa valores absolutos de porcentajes
- `pivotear_dataset()`: Transforma de formato largo a ancho
- `renombrar_columnas_gastos()` / `renombrar_columnas_fondos()`
- `consolidar_datasets()`: Une múltiples datasets
- `filtrar_periodo()`: Filtra por rango de años

### `src/visualization.py`
Funciones para visualizaciones:
- `configurar_estilo()`: Configura estilo de gráficos
- `plot_evolucion_temporal()`: Gráfico de evolución temporal
- `plot_distribucion_sectorial()`: Distribución por sectores
- `plot_origen_fondos()`: Análisis de origen de fondos
- `plot_impacto_eventos()`: Impacto de crisis económicas
- `plot_histograma_distribucion_gasto()`: Histogramas de distribución del gasto

## 📝 Decisiones de Diseño

### Arquitectura Modular
- **Separación de notebooks**: Cada fase del análisis en un notebook independiente
- **Funciones reutilizables**: Código en módulos Python (.py) en lugar de notebooks
- **Pipeline reproducible**: Cada notebook genera archivos para el siguiente

### Gestión de Datos
- **Valores faltantes**: Mantenidos como NaN (no imputación arbitraria)
- **Formato de datos**: Transformación a formato ancho para análisis temporal
- **Persistencia**: Guardado de resultados intermedios (consolidados, limpios)

### Calidad del Código
- **Funciones documentadas**: Docstrings con descripción, parámetros y retorno
- **Nombres descriptivos**: Variables y funciones autoexplicativas
- **Logging**: Prints informativos durante ejecución

## 🎓 Aprendizajes Clave

1. **Pipeline de datos completo**: Carga → Exploración → Limpieza → Análisis
2. **Código modular**: Separación de lógica de negocio (funciones) y análisis (notebooks)
3. **Tratamiento de datos reales**: Gestión de formatos no estándar, valores faltantes
4. **Visualización de datos**: Comunicación efectiva de insights mediante gráficos
5. **Documentación**: README profesional y código bien comentado

**Nota:** Los datos utilizados provienen del Instituto Nacional de Estadística (INE) y son de dominio público.