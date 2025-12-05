import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression

st.subheader("🔮 Prédictions de PM10, Température ou Humidité")

BG = "#F0F8FF"

plt.rcParams['figure.facecolor'] = BG
plt.rcParams['axes.facecolor'] = BG

sns.set_style("whitegrid", rc={
    "axes.facecolor": BG,
    "figure.facecolor": BG
})

# ----------------------------
# Chargement des données
# ----------------------------
df = pd.read_csv("qualiteair.csv", sep=';')

# ----------------------------
# Nettoyage et conversion numérique
# ----------------------------
for col in ["PM10", "TEMP", "HUMI"]:
    df[col] = (
        df[col]
        .astype(str)
        .str.replace(",", ".", regex=False)  # virgule → point
        .str.strip()
    )
    df[col] = pd.to_numeric(df[col], errors="coerce")  # convertit en float

# Filtrer lignes valides
df = df.dropna(subset=["PM10", "TEMP", "HUMI"])

# ----------------------------
# Choix de la variable cible
# ----------------------------
target = st.selectbox(
    "Choisir la variable à prédire :",
    ["PM10", "TEMP", "HUMI"]
)

# Définir X et y
features = [col for col in ["PM10", "TEMP", "HUMI"] if col != target]
X = df[features]
y = df[target]

# ----------------------------
# Modèle
# ----------------------------
model = LinearRegression()
model.fit(X, y)

# ----------------------------
# Interface utilisateur
# ----------------------------
st.write("Ajustez les valeurs pour prédire :", target)

val1 = st.slider(
    f"{features[0]}",
    float(X[features[0]].min()), float(X[features[0]].max()), float(X[features[0]].mean())
)

val2 = st.slider(
    f"{features[1]}",
    float(X[features[1]].min()), float(X[features[1]].max()), float(X[features[1]].mean())
)

input_data = np.array([[val1, val2]])
prediction = model.predict(input_data)[0]

# ----------------------------
# Résultat
# ----------------------------
st.markdown(f"### 🔎 Prédiction de **{target}** : `{prediction:.2f}`")

# ----------------------------
# Equation du modèle
# ----------------------------
coef1, coef2 = model.coef_
intercept = model.intercept_

st.markdown("### 📐 Équation du modèle")
st.write(f"{target} = {intercept:.2f} + ({coef1:.2f} × {features[0]}) + ({coef2:.2f} × {features[1]})")

st.info("Le modèle utilise une régression linéaire simple.")
