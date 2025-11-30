"""
Módulo de visualización para el proyecto EDA de I+D en España

Este módulo contiene funciones para generar visualizaciones
del análisis de inversión en I+D.
"""

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np


def configurar_estilo():
    """
    Configura el estilo general de las visualizaciones.
    """
    sns.set_style('whitegrid')
    plt.rcParams['figure.figsize'] = (14, 6)
    plt.rcParams['font.size'] = 10
    plt.rcParams['axes.titlesize'] = 14
    plt.rcParams['axes.labelsize'] = 11


def plot_evolucion_temporal(df_gastos_wide):
    """
    Genera gráfico de evolución temporal del gasto total en I+D.

    Args:
        df_gastos_wide (pd.DataFrame): DataFrame de gastos en formato ancho con índice de años
    """
    fig, ax = plt.subplots(figsize=(14, 6))

    # Gráfico de línea con marcadores
    ax.plot(df_gastos_wide.index, df_gastos_wide['Total']/1000,
            marker='o', linewidth=2.5, markersize=6, color='#2E86AB', label='Gasto Total I+D')

    # Marcar eventos importantes
    ax.axvline(x=2008, color='red', linestyle='--', linewidth=1.5, alpha=0.7, label='Crisis Financiera 2008')
    ax.axvline(x=2020, color='orange', linestyle='--', linewidth=1.5, alpha=0.7, label='Pandemia COVID-19')

    # Títulos y etiquetas
    ax.set_title('Evolución del Gasto Total en I+D en España (2000-2024)', fontsize=16, fontweight='bold', pad=20)
    ax.set_xlabel('Año', fontsize=12)
    ax.set_ylabel('Gasto en I+D (Millones de €)', fontsize=12)
    ax.legend(loc='upper left', frameon=True, shadow=True)
    ax.grid(True, alpha=0.3)

    # Formato del eje Y
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{x:,.0f}M €'))

    plt.tight_layout()
    plt.show()

    # Estadísticas descriptivas
    print("\n" + "="*70)
    print("ESTADÍSTICAS DEL GASTO TOTAL EN I+D (2000-2024)")
    print("="*70)
    print(f"\n💰 Gasto en 2000: {df_gastos_wide.loc[2000, 'Total']:,.0f} miles de €")
    print(f"💰 Gasto en 2024: {df_gastos_wide.loc[2024, 'Total']:,.0f} miles de €")
    print(f"\n📈 Crecimiento total: {((df_gastos_wide.loc[2024, 'Total'] / df_gastos_wide.loc[2000, 'Total']) - 1) * 100:.1f}%")
    print(f"📊 Gasto máximo: {df_gastos_wide['Total'].max():,.0f} miles de € (año {df_gastos_wide['Total'].idxmax()})")
    print(f"📉 Gasto mínimo: {df_gastos_wide['Total'].min():,.0f} miles de € (año {df_gastos_wide['Total'].idxmin()})")
    print(f"\n📊 Media del período: {df_gastos_wide['Total'].mean():,.0f} miles de €")
    print(f"📊 Desviación estándar: {df_gastos_wide['Total'].std():,.0f} miles de €")


def plot_distribucion_sectorial(df_gastos_wide):
    """
    Genera gráficos de distribución del gasto por sectores.

    Args:
        df_gastos_wide (pd.DataFrame): DataFrame de gastos en formato ancho
    """
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))

    # 1. Gráfico de áreas apiladas (valores absolutos)
    sectores_gastos = ['Admin_Publica', 'Enseñanza_Superior', 'Empresas', 'IPSFL']
    colores = ['#A23B72', '#F18F01', '#2E86AB', '#06A77D']

    ax1.stackplot(df_gastos_wide.index,
                  df_gastos_wide['Admin_Publica']/1000,
                  df_gastos_wide['Enseñanza_Superior']/1000,
                  df_gastos_wide['Empresas']/1000,
                  df_gastos_wide['IPSFL']/1000,
                  labels=['Administración Pública', 'Enseñanza Superior', 'Empresas', 'IPSFL'],
                  colors=colores, alpha=0.8)

    ax1.set_title('Evolución del Gasto en I+D por Sector (Valores Absolutos)', fontsize=14, fontweight='bold')
    ax1.set_xlabel('Año')
    ax1.set_ylabel('Gasto (Millones de €)')
    ax1.legend(loc='upper left', frameon=True)
    ax1.grid(True, alpha=0.3)
    ax1.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{x:,.0f}M'))

    # 2. Gráfico de barras para comparar 2000 vs 2024
    x = range(len(sectores_gastos))
    width = 0.35

    valores_2000 = [df_gastos_wide.loc[2000, col]/1000 for col in sectores_gastos]
    valores_2024 = [df_gastos_wide.loc[2024, col]/1000 for col in sectores_gastos]

    ax2.bar([i - width/2 for i in x], valores_2000, width, label='2000', color='#7A7D7D', alpha=0.8)
    ax2.bar([i + width/2 for i in x], valores_2024, width, label='2024', color='#2E86AB', alpha=0.8)

    ax2.set_title('Comparación del Gasto por Sector: 2000 vs 2024', fontsize=14, fontweight='bold')
    ax2.set_xlabel('Sector')
    ax2.set_ylabel('Gasto (Millones de €)')
    ax2.set_xticks(x)
    ax2.set_xticklabels(['Admin.\nPública', 'Enseñanza\nSuperior', 'Empresas', 'IPSFL'])
    ax2.legend()
    ax2.grid(True, alpha=0.3, axis='y')
    ax2.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{x:,.0f}M'))

    plt.tight_layout()
    plt.show()

    # Análisis cuantitativo
    print("\n" + "="*70)
    print("ANÁLISIS POR SECTORES (2000 vs 2024)")
    print("="*70)
    for sector in sectores_gastos:
        val_2000 = df_gastos_wide.loc[2000, sector]
        val_2024 = df_gastos_wide.loc[2024, sector]
        crecimiento = ((val_2024 / val_2000) - 1) * 100
        print(f"\n📊 {sector.replace('_', ' ').title()}:")
        print(f"   2000: {val_2000:,.0f} miles de €")
        print(f"   2024: {val_2024:,.0f} miles de €")
        print(f"   Crecimiento: {crecimiento:+.1f}%")


def plot_origen_fondos(df_fondos_wide):
    """
    Genera gráficos del origen de los fondos de I+D.

    Args:
        df_fondos_wide (pd.DataFrame): DataFrame de fondos en formato ancho
    """
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))

    # 1. Evolución temporal de fondos por origen
    sectores_fondos = ['Admin_Publica', 'Empresas', 'IPSFL', 'Resto_Mundo']
    colores_fondos = ['#A23B72', '#2E86AB', '#06A77D', '#F18F01']

    for sector, color in zip(sectores_fondos, colores_fondos):
        ax1.plot(df_fondos_wide.index, df_fondos_wide[sector]/1000,
                 marker='o', linewidth=2, label=sector.replace('_', ' ').title(), color=color)

    ax1.set_title('Evolución de los Fondos de I+D por Origen (2000-2024)', fontsize=14, fontweight='bold')
    ax1.set_xlabel('Año')
    ax1.set_ylabel('Fondos (Millones de €)')
    ax1.legend(loc='upper left', frameon=True)
    ax1.grid(True, alpha=0.3)
    ax1.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{x:,.0f}M'))

    # 2. Gráfico de torta para 2024
    valores_fondos_2024 = [df_fondos_wide.loc[2024, col] for col in sectores_fondos]
    labels_fondos = ['Administración\nPública', 'Empresas', 'IPSFL', 'Resto del\nMundo']

    ax2.pie(valores_fondos_2024, labels=labels_fondos, autopct='%1.1f%%',
            colors=colores_fondos, startangle=90, textprops={'fontsize': 11})
    ax2.set_title('Distribución de Fondos de I+D en 2024', fontsize=14, fontweight='bold')

    plt.tight_layout()
    plt.show()

    # Estadísticas
    print("\n" + "="*70)
    print("ORIGEN DE LOS FONDOS (2024)")
    print("="*70)
    total_fondos_2024 = df_fondos_wide.loc[2024, 'Total']
    for sector in sectores_fondos:
        valor = df_fondos_wide.loc[2024, sector]
        porcentaje = (valor / total_fondos_2024) * 100
        print(f"\n💰 {sector.replace('_', ' ').title()}: {valor:,.0f} miles de € ({porcentaje:.1f}%)")


def plot_impacto_eventos(df_gastos_wide):
    """
    Genera gráficos del impacto de eventos económicos en I+D.

    Args:
        df_gastos_wide (pd.DataFrame): DataFrame de gastos en formato ancho
    """
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))

    # 1. Impacto de la Crisis de 2008
    años_crisis = range(2006, 2015)
    gastos_crisis = [df_gastos_wide.loc[año, 'Total']/1000 for año in años_crisis]

    ax1.plot(años_crisis, gastos_crisis, marker='o', linewidth=2.5, markersize=8, color='#2E86AB')
    ax1.axvline(x=2008, color='red', linestyle='--', linewidth=2, alpha=0.7, label='Inicio Crisis 2008')
    ax1.fill_between(años_crisis, gastos_crisis, alpha=0.3, color='#2E86AB')

    ax1.set_title('Impacto de la Crisis Financiera de 2008 en I+D', fontsize=14, fontweight='bold')
    ax1.set_xlabel('Año')
    ax1.set_ylabel('Gasto en I+D (Millones de €)')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    ax1.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{x:,.0f}M'))

    # 2. Impacto de COVID-19 (2020)
    años_covid = range(2018, 2025)
    gastos_covid = [df_gastos_wide.loc[año, 'Total']/1000 for año in años_covid]

    ax2.plot(años_covid, gastos_covid, marker='o', linewidth=2.5, markersize=8, color='#06A77D')
    ax2.axvline(x=2020, color='orange', linestyle='--', linewidth=2, alpha=0.7, label='Pandemia COVID-19')
    ax2.fill_between(años_covid, gastos_covid, alpha=0.3, color='#06A77D')

    ax2.set_title('Impacto de la Pandemia COVID-19 en I+D', fontsize=14, fontweight='bold')
    ax2.set_xlabel('Año')
    ax2.set_ylabel('Gasto en I+D (Millones de €)')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    ax2.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{x:,.0f}M'))

    plt.tight_layout()
    plt.show()

    # Análisis cuantitativo
    print("\n" + "="*70)
    print("IMPACTO DE LA CRISIS DE 2008")
    print("="*70)
    print(f"\n💰 Gasto en 2008: {df_gastos_wide.loc[2008, 'Total']:,.0f} miles de €")
    print(f"💰 Gasto en 2013 (punto más bajo): {df_gastos_wide.loc[2013, 'Total']:,.0f} miles de €")
    caida_crisis = ((df_gastos_wide.loc[2013, 'Total'] / df_gastos_wide.loc[2008, 'Total']) - 1) * 100
    print(f"📉 Variación 2008-2013: {caida_crisis:.1f}%")

    print("\n" + "="*70)
    print("IMPACTO DE LA PANDEMIA COVID-19")
    print("="*70)
    print(f"\n💰 Gasto en 2019: {df_gastos_wide.loc[2019, 'Total']:,.0f} miles de €")
    print(f"💰 Gasto en 2020: {df_gastos_wide.loc[2020, 'Total']:,.0f} miles de €")
    print(f"💰 Gasto en 2021: {df_gastos_wide.loc[2021, 'Total']:,.0f} miles de €")
    var_2020 = ((df_gastos_wide.loc[2020, 'Total'] / df_gastos_wide.loc[2019, 'Total']) - 1) * 100
    var_2021 = ((df_gastos_wide.loc[2021, 'Total'] / df_gastos_wide.loc[2020, 'Total']) - 1) * 100
    print(f"📊 Variación 2019-2020: {var_2020:+.1f}%")
    print(f"📈 Variación 2020-2021: {var_2021:+.1f}%")
    

def plot_histograma_distribucion_gasto(df_gastos_wide):
    """
    Genera histograma de la distribución del gasto total en I+D.

    Args:
        df_gastos_wide (pd.DataFrame): DataFrame de gastos en formato ancho con índice de años
    """
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))

    # 1. Histograma del gasto total
    ax1.hist(df_gastos_wide['Total']/1000, bins=15, color='#2E86AB', alpha=0.7, edgecolor='black')
    ax1.axvline(df_gastos_wide['Total'].mean()/1000, color='red', linestyle='--', linewidth=2, label=f'Media: {df_gastos_wide["Total"].mean()/1000:.0f}M €')
    ax1.axvline(df_gastos_wide['Total'].median()/1000, color='orange', linestyle='--', linewidth=2, label=f'Mediana: {df_gastos_wide["Total"].median()/1000:.0f}M €')
    
    ax1.set_title('Distribución del Gasto Total en I+D (2000-2024)', fontsize=14, fontweight='bold')
    ax1.set_xlabel('Gasto Total (Millones de €)')
    ax1.set_ylabel('Número de años')
    ax1.legend()
    ax1.grid(True, alpha=0.3, axis='y')

    # 2. Histograma del crecimiento interanual
    crecimiento = df_gastos_wide['Total'].pct_change() * 100
    crecimiento = crecimiento.dropna()
    
    ax2.hist(crecimiento, bins=12, color='#06A77D', alpha=0.7, edgecolor='black')
    ax2.axvline(0, color='red', linestyle='-', linewidth=2, alpha=0.5, label='Sin crecimiento')
    ax2.axvline(crecimiento.mean(), color='orange', linestyle='--', linewidth=2, label=f'Media: {crecimiento.mean():.1f}%')
    
    ax2.set_title('Distribución del Crecimiento Interanual en I+D', fontsize=14, fontweight='bold')
    ax2.set_xlabel('Crecimiento Interanual (%)')
    ax2.set_ylabel('Número de años')
    ax2.legend()
    ax2.grid(True, alpha=0.3, axis='y')

    plt.tight_layout()
    plt.show()

    # Estadísticas
    print("\n" + "="*70)
    print("ANÁLISIS DE DISTRIBUCIÓN")
    print("="*70)
    print(f"\n📊 Distribución del gasto total:")
    print(f"   Media: {df_gastos_wide['Total'].mean():,.0f} miles de €")
    print(f"   Mediana: {df_gastos_wide['Total'].median():,.0f} miles de €")
    print(f"   Desviación estándar: {df_gastos_wide['Total'].std():,.0f} miles de €")
    print(f"   Rango: {df_gastos_wide['Total'].min():,.0f} - {df_gastos_wide['Total'].max():,.0f} miles de €")
    
    print(f"\n📈 Distribución del crecimiento interanual:")
    print(f"   Media: {crecimiento.mean():.2f}%")
    print(f"   Mediana: {crecimiento.median():.2f}%")
    print(f"   Desviación estándar: {crecimiento.std():.2f}%")
    print(f"   Rango: {crecimiento.min():.2f}% - {crecimiento.max():.2f}%")