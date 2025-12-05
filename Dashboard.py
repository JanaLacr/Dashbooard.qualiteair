import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from math import pi
from matplotlib.cm import get_cmap
from sklearn.linear_model import LinearRegression

# ==========================
# Fond graphique personnalisé
# ==========================
BG = "#F0F8FF"   # secondaryBackgroundColor du thème

plt.rcParams['figure.facecolor'] = BG
plt.rcParams['axes.facecolor'] = BG

sns.set_style("whitegrid", rc={
    "axes.facecolor": BG,
    "figure.facecolor": BG
})

# ==========================
# Configuration de la page
# ==========================
st.set_page_config(
    page_title="Analyse de la qualité de l'air – Saint-Germain-des-Prés",
    layout="wide"
)

# ----------------------------
# Chargement des données
# ----------------------------
df = pd.read_csv("qualiteair.csv", sep=';')

# Correction des décimales (virgule → point)
for col in ['TEMP', 'HUMI', 'PM10']:
    df[col] = df[col].astype(str).str.replace(",", ".")
    df[col] = pd.to_numeric(df[col], errors='coerce')

# Convertir DATE/HEURE en datetime
df["DATE/HEURE"] = pd.to_datetime(df["DATE/HEURE"], errors="coerce")

# ----------------------------
# Interface Streamlit
# ----------------------------
st.title("🌫️ Analyse de la qualité de l’air – Saint-Germain-des-Prés")
st.write("Application générée automatiquement à partir du fichier **qualiteair.csv**.")

# Sidebar
st.sidebar.header("Options d'affichage")
option = st.sidebar.selectbox(
    "Choisissez une variable à visualiser",
    ["PM10", "TEMP", "HUMI"]
)

# ==========================
# Fonctions graphiques
# ==========================
def plot_time_series(column_name, ylabel):
    fig, ax = plt.subplots()
    ax.plot(df["DATE/HEURE"], df[column_name])
    ax.set_title(f"Évolution de {ylabel} dans le temps")
    ax.set_xlabel("Date")
    ax.set_ylabel(ylabel)
    plt.xticks(rotation=45)
    st.pyplot(fig)

def plot_boxplot(column_name, ylabel):
    fig, ax = plt.subplots()
    sns.boxplot(x=df[column_name], ax=ax)
    ax.set_title(f"Distribution de {ylabel}")
    ax.set_xlabel(ylabel)
    st.pyplot(fig)

# ==========================
# AFFICHAGE SELON L’OPTION
# ==========================

# ----------- PM10 -----------
if option == "PM10":
    st.subheader("🟦 Évolution des particules PM10")

    pm10_moy = df["PM10"].mean()
    pm10_max = df["PM10"].max()
    pm10_min = df["PM10"].min()

    col1, col2, col3 = st.columns(3)
    col1.metric("😷 PM10 moyenne", f"{pm10_moy:.2f} µg/m³")
    col2.metric("😷 PM10 max", f"{pm10_max:.2f} µg/m³")
    col3.metric("😷 PM10 min", f"{pm10_min:.2f} µg/m³")

    plot_time_series("PM10", "PM10 (µg/m³)")

    corr_text = (
        "Dans ce graphique montrant l'évolution PM10 au cours des mois en 2025, "
        "on peut constater une évolution constante avec certains pics."
    )
    st.write(corr_text)

    plot_boxplot("PM10", "PM10 (µg/m³)")

    st.write(df["PM10"].describe())

# ----------- TEMPÉRATURE -----------
elif option == "TEMP":
    st.subheader("🌡️ Évolution de la température")

    temp_moy = df["TEMP"].mean()
    temp_max = df["TEMP"].max()
    temp_min = df["TEMP"].min()

    col1, col2, col3 = st.columns(3)
    col1.metric("🌡 Température moyenne", f"{temp_moy:.2f} °C")
    col2.metric("🌡 Température max", f"{temp_max:.2f} °C")
    col3.metric("🌡 Température min", f"{temp_min:.2f} °C")

    plot_time_series("TEMP", "Température (°C)")

    corr_text = (
        "Dans ce graphique montrant l'évolution de la température en 2025, "
        "on observe une hausse de février à juillet puis une baisse progressive."
    )
    st.write(corr_text)

    plot_boxplot("TEMP", "Température (°C)")

    st.write(df["TEMP"].describe())

# ----------- HUMIDITÉ -----------
elif option == "HUMI":
    st.subheader("💧 Évolution de l'humidité")

    humi_moy = df["HUMI"].mean()
    humi_max = df["HUMI"].max()
    humi_min = df["HUMI"].min()

    col1, col2, col3 = st.columns(3)
    col1.metric("💧 Humidité moyenne", f"{humi_moy:.2f} %")
    col2.metric("💧 Humidité max", f"{humi_max:.2f} %")
    col3.metric("💧 Humidité min", f"{humi_min:.2f} %")

    plot_time_series("HUMI", "Humidité (%)")

    corr_text = (
        "L'humidité présente une évolution assez stable, avec un pic important en mars 2025."
    )
    st.write(corr_text)

    plot_boxplot("HUMI", "Humidité (%)")

    st.write(df["HUMI"].describe())


# ----------------------------
# Données brutes
# ----------------------------
st.subheader("📄 Aperçu des données brutes")
st.dataframe(df)
