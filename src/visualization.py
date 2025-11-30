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

    bars_2000 = ax2.bar([i - width/2 for i in x], valores_2000, width, label='2000', color='#7A7D7D', alpha=0.8)
    bars_2024 = ax2.bar([i + width/2 for i in x], valores_2024, width, label='2024', color='#2E86AB', alpha=0.8)

    # Añadir etiquetas con el aumento en cada sector
    for i, sector in enumerate(sectores_gastos):
        val_2000 = valores_2000[i]
        val_2024 = valores_2024[i]
        aumento_millones = val_2024 - val_2000
        multiplicador = val_2024 / val_2000

        # Etiqueta sobre la barra de 2024
        ax2.text(i + width/2, val_2024 + max(valores_2024) * 0.02,
                f'+{aumento_millones:.0f}M €\n(x{multiplicador:.1f})',
                ha='center', va='bottom', fontsize=9, fontweight='bold', color='#2E86AB')

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
    

def plot_histograma_distribucion_gasto(df_gastos_wide, df_fondos_wide):
    """
    Genera análisis de Fondos vs Gastos en I+D por sector, mostrando tabla año por año y histograma del ratio.

    Args:
        df_gastos_wide (pd.DataFrame): DataFrame de gastos en formato ancho con índice de años
        df_fondos_wide (pd.DataFrame): DataFrame de fondos en formato ancho con índice de años
    """
    # Sectores a analizar
    sectores = ['Empresas', 'Admin_Publica']
    nombres_sectores = {'Empresas': 'EMPRESAS', 'Admin_Publica': 'ADMINISTRACIÓN PÚBLICA'}
    colores_sectores = {'Empresas': '#2E86AB', 'Admin_Publica': '#A23B72'}

    # Crear tabla comparativa para cada sector
    for sector in sectores:
        print("\n" + "="*100)
        print(f"TABLA COMPARATIVA: FONDOS VS GASTOS - SECTOR {nombres_sectores[sector]} (miles de €)")
        print("="*100)
        print(f"{'Año':<6} {'Fondos':>15} {'Gastos':>15} {'Diferencia':>15} {'Ratio (%)':>15}")
        print("-"*100)

        for año in df_gastos_wide.index:
            gastos = df_gastos_wide.loc[año, sector]
            fondos = df_fondos_wide.loc[año, sector]
            diferencia = fondos - gastos
            ratio = (fondos / gastos) * 100

            simbolo = "+" if diferencia > 0 else ""

            print(f"{año:<6} {fondos:>15,.0f} {gastos:>15,.0f} {simbolo}{diferencia:>14,.0f} {ratio:>14,.2f}%")

        print("="*100)

    # Crear visualización separada para cada sector
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))

    # Calcular ratios para ambos sectores
    datos_sectores = {}
    for sector in sectores:
        ratios_sector = []
        for año in df_gastos_wide.index:
            ratio = (df_fondos_wide.loc[año, sector] / df_gastos_wide.loc[año, sector]) * 100
            ratios_sector.append(ratio)
        datos_sectores[sector] = ratios_sector

    # Visualización para cada sector
    for idx, sector in enumerate(sectores):
        ax_hist = axes[idx, 0]
        ax_evol = axes[idx, 1]

        color = colores_sectores[sector]
        nombre = nombres_sectores[sector]
        ratios = datos_sectores[sector]

        # Calcular rango específico para este sector
        rango_min = min(ratios)
        rango_max = max(ratios)
        margen = (rango_max - rango_min) * 0.1  # 10% de margen

        # 1. Histograma de distribución
        ax_hist.hist(ratios, bins=12, color=color, alpha=0.7, edgecolor='black',
                    range=(rango_min - margen, rango_max + margen))
        ax_hist.axvline(x=100, color='red', linestyle='--', linewidth=2, alpha=0.7)
        ax_hist.axvline(x=pd.Series(ratios).mean(), color='green', linestyle='--',
                       linewidth=2, alpha=0.7, label=f'Media ({pd.Series(ratios).mean():.1f}%)')

        ax_hist.set_xlim(rango_min - margen, rango_max + margen)
        ax_hist.set_title(f'Distribución del Ratio Fondos/Gastos - {nombre.title()} (2000-2024)',
                         fontsize=13, fontweight='bold')
        ax_hist.set_xlabel('Ratio Fondos/Gastos (%)')
        ax_hist.set_ylabel('Número de años')
        ax_hist.legend(fontsize=9)
        ax_hist.grid(True, alpha=0.3, axis='y')

        # 2. Evolución temporal
        ax_evol.plot(df_gastos_wide.index, ratios, marker='o', linewidth=2.5,
                    label=nombre.title(), color=color, markersize=6)

        ax_evol.axhline(y=100, color='red', linestyle='--', linewidth=2, alpha=0.7,
                       label='Equilibrio (100%)')
        ax_evol.axvline(x=2008, color='red', linestyle=':', linewidth=1.5, alpha=0.5,
                       label='Crisis 2008')
        ax_evol.axvline(x=2020, color='orange', linestyle=':', linewidth=1.5, alpha=0.5,
                       label='COVID-19')

        ax_evol.set_title(f'Evolución Temporal del Ratio Fondos/Gastos - {nombre.title()}',
                         fontsize=13, fontweight='bold')
        ax_evol.set_xlabel('Año')
        ax_evol.set_ylabel('Ratio Fondos/Gastos (%)')
        ax_evol.legend(loc='best', fontsize=9)
        ax_evol.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.show()

    # Estadísticas resumen para cada sector
    for sector in sectores:
        print("\n" + "="*70)
        print(f"RESUMEN ESTADÍSTICO - SECTOR {nombres_sectores[sector]}")
        print("="*70)

        ratios_sector = []
        diferencias_sector = []

        for año in df_gastos_wide.index:
            gastos = df_gastos_wide.loc[año, sector]
            fondos = df_fondos_wide.loc[año, sector]
            ratio = (fondos / gastos) * 100
            diferencia = fondos - gastos

            ratios_sector.append(ratio)
            diferencias_sector.append(diferencia)

        ratios_sector = pd.Series(ratios_sector)
        diferencias_sector = pd.Series(diferencias_sector)

        print(f"\n{'='*70}")
        print(f"📊 {nombres_sectores[sector]}")
        print("-"*70)
        print(f"   Ratio medio: {ratios_sector.mean():.2f}%")
        print(f"   Ratio mediano: {ratios_sector.median():.2f}%")
        print(f"   Desviación estándar: {ratios_sector.std():.2f}%")
        print(f"   Rango: {ratios_sector.min():.2f}% - {ratios_sector.max():.2f}%")

        print(f"\n   Diferencia media: {diferencias_sector.mean():,.0f} miles de €")
        print(f"   Diferencia mediana: {diferencias_sector.median():,.0f} miles de €")

        años_superavit = (ratios_sector > 100).sum()
        print(f"\n   Años con más fondos que gastos: {años_superavit}/25 ({años_superavit/25*100:.1f}%)")