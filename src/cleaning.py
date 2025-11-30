"""
Módulo de limpieza de datos para el proyecto EDA de I+D en España

Este módulo contiene funciones para limpiar y transformar los datos
del Instituto Nacional de Estadística (INE) sobre inversión en I+D.
"""

import pandas as pd
import numpy as np


def limpiar_columna_total(df, nombre_dataset="Dataset"):
    """
    Limpia la columna 'Total' convirtiendo formato numérico europeo a estándar.

    Pasos:
    1. Reemplaza ".." (dato no disponible) por NaN
    2. Elimina puntos (separador de miles)
    3. Reemplaza comas por puntos (separador decimal)
    4. Convierte a tipo float

    Args:
        df (pd.DataFrame): DataFrame con columna 'Total' en formato texto europeo
        nombre_dataset (str): Nombre descriptivo del dataset para logs

    Returns:
        pd.DataFrame: DataFrame con columna 'Total' limpia en formato numérico
    """
    df_limpio = df.copy()

    print(f"\n🧹 Limpiando columna 'Total' de {nombre_dataset}...")
    print(f"   Tipo original: {df_limpio['Total'].dtype}")

    # Contar valores ".." antes de limpiar
    valores_faltantes = (df_limpio['Total'] == '..').sum()
    if valores_faltantes > 0:
        print(f"   Valores '..' encontrados: {valores_faltantes}")

    # Paso 1: Reemplazar ".." con NaN
    df_limpio['Total'] = df_limpio['Total'].replace('..', np.nan)

    # Paso 2: Eliminar puntos (separador de miles)
    df_limpio['Total'] = df_limpio['Total'].str.replace('.', '', regex=False)

    # Paso 3: Reemplazar comas por puntos (separador decimal)
    df_limpio['Total'] = df_limpio['Total'].str.replace(',', '.', regex=False)

    # Paso 4: Convertir a float
    df_limpio['Total'] = pd.to_numeric(df_limpio['Total'], errors='coerce')

    print(f"   Tipo final: {df_limpio['Total'].dtype}")
    print(f"   Valores NaN: {df_limpio['Total'].isna().sum()}")

    return df_limpio


def separar_valores_porcentajes(df):
    """
    Separa valores absolutos de porcentajes en datasets de I+D.

    Los datasets del INE mezclan valores absolutos (miles de euros) con
    porcentajes en la columna 'Sectores/unidad'. Esta función los separa.

    Args:
        df (pd.DataFrame): DataFrame con valores absolutos y porcentajes mezclados

    Returns:
        pd.DataFrame: DataFrame solo con valores absolutos (sin porcentajes)
    """
    print("\n📊 Separando valores absolutos de porcentajes...")

    # Identificar filas con porcentajes (contienen "%")
    filas_porcentaje = df['Sectores/unidad'].str.contains('%', na=False)

    print(f"   Filas con porcentajes: {filas_porcentaje.sum()}")
    print(f"   Filas con valores absolutos: {(~filas_porcentaje).sum()}")

    # Mantener solo valores absolutos
    df_valores = df[~filas_porcentaje].copy()

    return df_valores


def pivotear_dataset(df, nombre_dataset="Dataset"):
    """
    Transforma dataset de formato largo a formato ancho para análisis temporal.

    Formato largo: múltiples filas por año (una por sector)
    Formato ancho: una fila por año, sectores como columnas

    Args:
        df (pd.DataFrame): DataFrame en formato largo
        nombre_dataset (str): Nombre descriptivo para logs

    Returns:
        pd.DataFrame: DataFrame en formato ancho con años como índice
    """
    print(f"\n🔄 Transformando {nombre_dataset} de formato largo a ancho...")
    print(f"   Dimensiones originales: {df.shape}")

    # Realizar pivot
    df_pivot = df.pivot(
        index='Años',
        columns='Sectores/unidad',
        values='Total'
    )

    # Reset para que Años sea columna
    df_pivot = df_pivot.reset_index()

    print(f"   Dimensiones después de pivot: {df_pivot.shape}")
    print(f"   Columnas creadas: {list(df_pivot.columns)}")

    return df_pivot


def renombrar_columnas_gastos(df):
    """
    Renombra columnas del dataset de gastos para mayor claridad.

    Args:
        df (pd.DataFrame): DataFrame de gastos con nombres largos

    Returns:
        pd.DataFrame: DataFrame con nombres de columnas simplificados
    """
    renombrado = {
        'Total (miles de euros)': 'Total',
        'Administración Pública: Total (miles de euros)': 'Admin_Publica',
        'Enseñanza Superior: Total (miles de euros)': 'Enseñanza_Superior',
        'Empresas: Total (miles de euros)': 'Empresas',
        'IPSFL: Total (miles de euros)': 'IPSFL'
    }

    df_renombrado = df.rename(columns=renombrado)

    print("\n✏️  Columnas renombradas:")
    for old, new in renombrado.items():
        if old in df.columns:
            print(f"   '{old}' → '{new}'")

    return df_renombrado


def renombrar_columnas_fondos(df):
    """
    Renombra columnas del dataset de fondos para mayor claridad.

    Args:
        df (pd.DataFrame): DataFrame de fondos con nombres largos

    Returns:
        pd.DataFrame: DataFrame con nombres de columnas simplificados
    """
    renombrado = {
        'Total (miles de euros)': 'Total',
        'Administración Pública: Total (miles de euros)': 'Admin_Publica',
        'Empresas: Total (miles de euros)': 'Empresas',
        'IPSFL: Total (miles de euros)': 'IPSFL',
        'Resto del Mundo: Total (miles de euros)': 'Resto_Mundo'
    }

    df_renombrado = df.rename(columns=renombrado)

    print("\n✏️  Columnas renombradas:")
    for old, new in renombrado.items():
        if old in df.columns:
            print(f"   '{old}' → '{new}'")

    return df_renombrado


def consolidar_datasets(df1, df2, año_duplicado=2021, nombre="Dataset"):
    """
    Consolida dos datasets eliminando años duplicados.

    Args:
        df1 (pd.DataFrame): Primer dataset (período antiguo)
        df2 (pd.DataFrame): Segundo dataset (período reciente)
        año_duplicado (int): Año que aparece en ambos datasets
        nombre (str): Nombre descriptivo

    Returns:
        pd.DataFrame: Dataset consolidado sin duplicados
    """
    print(f"\n🔗 Consolidando {nombre}...")
    print(f"   Dataset 1: {df1.shape[0]} filas")
    print(f"   Dataset 2: {df2.shape[0]} filas")

    # Eliminar año duplicado del segundo dataset
    df2_sin_duplicado = df2[df2['Años'] != año_duplicado].copy()
    print(f"   Eliminando año {año_duplicado} del dataset 2")

    # Concatenar
    df_consolidado = pd.concat([df1, df2_sin_duplicado], ignore_index=True)

    # Convertir Años a numérico
    df_consolidado['Años'] = pd.to_numeric(df_consolidado['Años'], errors='coerce')

    # Ordenar por año
    df_consolidado = df_consolidado.sort_values('Años').reset_index(drop=True)

    print(f"   Dataset consolidado: {df_consolidado.shape[0]} filas")
    print(f"   Rango de años: {df_consolidado['Años'].min():.0f} - {df_consolidado['Años'].max():.0f}")

    return df_consolidado


def filtrar_periodo(df, año_inicio=2000, año_fin=2024):
    """
    Filtra dataset por un rango de años específico.

    Args:
        df (pd.DataFrame): DataFrame con columna 'Años'
        año_inicio (int): Año inicial del período
        año_fin (int): Año final del período

    Returns:
        pd.DataFrame: DataFrame filtrado
    """
    print(f"\n📅 Filtrando período {año_inicio}-{año_fin}...")
    print(f"   Filas antes de filtrar: {df.shape[0]}")

    df_filtrado = df[
        (df['Años'] >= año_inicio) &
        (df['Años'] <= año_fin)
    ].copy()

    print(f"   Filas después de filtrar: {df_filtrado.shape[0]}")

    return df_filtrado


def preparar_para_indice(df):
    """
    Prepara DataFrame para usar Años como índice.

    Args:
        df (pd.DataFrame): DataFrame con columna 'Años'

    Returns:
        pd.DataFrame: DataFrame con 'Años' como índice
    """
    df_con_indice = df.set_index('Años')
    print(f"\n🔑 'Años' establecido como índice")
    print(f"   Índice: {df_con_indice.index.min():.0f} - {df_con_indice.index.max():.0f}")

    return df_con_indice