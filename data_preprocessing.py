import pandas as pd
import streamlit as st

# Lade die CSV-Dateien
def load_data():
    life_expectancy_df = pd.read_csv("../data/life_expectancy.csv")
    population_df = pd.read_csv("../data/population.csv")
    gni_df = pd.read_csv("../data/gni_per_capita.csv")
    return life_expectancy_df, population_df, gni_df

# Fehlende Werte mit Forward Fill auffüllen und in Tidy Format umwandeln
def preprocess_data(life_expectancy_df, population_df, gni_df):
    # Fehlende Werte mit Forward Fill auffüllen
    life_expectancy_df.fillna(method='ffill', inplace=True)
    population_df.fillna(method='ffill', inplace=True)
    gni_df.fillna(method='ffill', inplace=True)

    # Umwandlung in tidy data format
    life_expectancy_df = life_expectancy_df.melt(id_vars=['country'], var_name='year', value_name='life_expectancy')
    population_df = population_df.melt(id_vars=['country'], var_name='year', value_name='population')
    gni_df = gni_df.melt(id_vars=['country'], var_name='year', value_name='gni_per_capita')

    # Konvertiere 'year' in Integer
    life_expectancy_df['year'] = life_expectancy_df['year'].astype(int)
    population_df['year'] = population_df['year'].astype(int)
    gni_df['year'] = gni_df['year'].astype(int)

    # Zusammenführen der drei DataFrames
    df = pd.merge(life_expectancy_df, population_df, on=['country', 'year'])
    df = pd.merge(df, gni_df, on=['country', 'year'])

    return df

# Die Funktion zum Laden und Vorverarbeiten der Daten
def load_and_process_data():
    life_expectancy_df, population_df, gni_df = load_data()
    df = preprocess_data(life_expectancy_df, population_df, gni_df)
    return df

# Caching der Daten
@st.cache_data
def get_data():
    return load_and_process_data()
