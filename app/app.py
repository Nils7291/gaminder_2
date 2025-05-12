import streamlit as st
import pandas as pd
import plotly.express as px
import sys
import numpy as np
import time
from data_preprocessing import get_data

# Funktion zum Umwandeln der Population in numerische Werte
def convert_population(population):
    try:
        if 'M' in population:
            return float(population.replace('M', '').strip()) * 1e6  # Millionen in numerische Werte umwandeln
        elif 'B' in population:
            return float(population.replace('B', '').strip()) * 1e9  # Milliarden in numerische Werte umwandeln
        elif 'K' in population:
            return float(population.replace('K', '').strip()) * 1e3  # Tausende in numerische Werte umwandeln
        else:
            return float(population.replace(',', '').strip())  # Für bereits numerische Werte (mit Komma entfernen)
    except ValueError:
        return 0  # Falls der Wert nicht umgewandelt werden kann, setzen wir ihn auf 0

# Funktion zum Umwandeln der GNI per capita in numerische Werte
def convert_gni(gni):
    try:
        if 'M' in gni:
            return float(gni.replace('M', '').strip()) * 1e6  # Millionen in numerische Werte umwandeln
        elif 'B' in gni:
            return float(gni.replace('B', '').strip()) * 1e9  # Milliarden in numerische Werte umwandeln
        elif 'K' in gni:
            return float(gni.replace('K', '').strip()) * 1e3  # Tausende in numerische Werte umwandeln
        else:
            return float(gni.replace(',', '').strip())  # Für bereits numerische Werte (mit Komma entfernen)
    except ValueError:
        return 0  # Falls der Wert nicht umgewandelt werden kann, setzen wir ihn auf 0

# Daten aus der data_preprocessing.py Datei laden
df = get_data()

# Bereinigung der Spalten 'population' und 'gni_per_capita'
df['population'] = df['population'].apply(convert_population)
df['gni_per_capita'] = df['gni_per_capita'].apply(convert_gni)

# Titel und Einführungstext hinzufügen
st.title("Gapminder Dashboard: Visualisierung von Lebensstandard und Gesundheit")
st.write("""
Willkommen zum Gapminder Dashboard! Diese interaktive Visualisierung zeigt den Zusammenhang 
zwischen dem Bruttonationalprodukt (BNE) pro Kopf, der Lebenserwartung und der Bevölkerung 
von verschiedenen Ländern zwischen 1990 und 2023.

Verwenden Sie den Slider, um ein Jahr auszuwählen und sehen Sie, wie sich die Blasen in Bezug 
auf Lebensstandard und Gesundheit über die Jahre entwickeln. Wählen Sie mehrere Länder aus, 
um diese im selben Diagramm zu vergleichen.

Klicken Sie auf den 'Play'-Button, um die Entwicklung der ausgewählten Länder von Jahr zu Jahr 
zu beobachten.
""")

# Jahr-Slider
year_slider = st.slider('Wählen Sie ein Jahr', min_value=int(df['year'].min()), 
                        max_value=int(df['year'].max()), value=2023)

# Multi-Select für Länder
selected_countries = st.multiselect('Wählen Sie ein oder mehrere Länder', df['country'].unique())

# Daten für das ausgewählte Jahr filtern
filtered_df = df[(df['year'] == year_slider) & (df['country'].isin(selected_countries))]

# Logarithmische Transformation der GNI-Werte
filtered_df['log_gni'] = np.log(filtered_df['gni_per_capita'].replace(0, np.nan))

# Blasendiagramm erstellen
fig = px.scatter(filtered_df, 
                 x='log_gni', 
                 y='life_expectancy', 
                 size='population', 
                 color='country', 
                 hover_name='country', 
                 size_max=60, 
                 log_x=True, 
                 title=f'Gapminder Dashboard - Jahr {year_slider}')

# Platzhalter für das Diagramm
chart_placeholder = st.empty()  # Platzhalter für das Diagramm
chart_placeholder.plotly_chart(fig)  # Start-Diagramm wird angezeigt

# Play-Button
play_button = st.button('Play')

# Wenn Play-Button geklickt wird, starte die Animation
if play_button:
    # Iteriere durch die Jahre von 1990 bis 2023
    for year in range(1990, 2024):
        st.session_state.year_slider_value = year

        # Daten für das aktuelle Jahr filtern
        filtered_df = df[(df['year'] == year) & (df['country'].isin(selected_countries))]

        # Logarithmische Transformation der GNI-Werte
        filtered_df['log_gni'] = np.log(filtered_df['gni_per_capita'].replace(0, np.nan))

        # Blasendiagramm erstellen
        fig = px.scatter(filtered_df, 
                         x='log_gni', 
                         y='life_expectancy', 
                         size='population', 
                         color='country', 
                         hover_name='country', 
                         size_max=60, 
                         log_x=True, 
                         title=f'Gapminder Dashboard - Jahr {year}')
        
        # Diagramm im Platzhalter aktualisieren
        chart_placeholder.plotly_chart(fig)

        # 0.25 Sekunde Pause zwischen den Jahren
        time.sleep(0.25)
