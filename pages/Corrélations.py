import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# ----------------------------
# Thème graphique
# ----------------------------
BG = "#F0F8FF"   # secondaryBackgroundColor du thème

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
# Nettoyage / Conversion numérique
# ----------------------------
for col in ['PM10', 'TEMP', 'HUMI']:
    df[col] = (
        df[col]
        .astype(str)               # convertit tout en chaîne pour nettoyer
        .str.replace(',', '.', regex=False)  # remplace virgules → points
        .str.strip()               # enlève les espaces éventuels
    )
    df[col] = pd.to_numeric(df[col], errors='coerce')

# ----------------------------
# Titre
# ----------------------------
st.subheader("📊 Corrélations entre PM10, Température et Humidité")

# ----------------------------
# Matrice de corrélation
# ----------------------------
fig, ax = plt.subplots()
corr = df[['PM10', 'TEMP', 'HUMI']].corr()

im = ax.imshow(corr, cmap="coolwarm")
plt.colorbar(im)

ax.set_xticks(range(len(corr.columns)))
ax.set_yticks(range(len(corr.columns)))
ax.set_xticklabels(corr.columns)
ax.set_yticklabels(corr.columns)

st.pyplot(fig)

# Texte interprétation
corr_text = (
    "Les corrélations observées sont faibles à modérées :\n"
    "- PM10 / TEMP : légèrement positive (~0.1)\n"
    "- PM10 / HUMI : légèrement négative (~-0.1)\n"
    "- TEMP / HUMI : modérément négative (~-0.3)\n"
)
st.write(corr_text)

# ----------------------------
# Comparatif Barplot
# ----------------------------
# ----------------------------
# Comparatif Barplot (Dégradé de bleu)
# ----------------------------
stats = {
    'PM10 (µg/m³)': [df['PM10'].mean(), df['PM10'].max(), df['PM10'].min()],
    'Température (°C)': [df['TEMP'].mean(), df['TEMP'].max(), df['TEMP'].min()],
    'Humidité (%)': [df['HUMI'].mean(), df['HUMI'].max(), df['HUMI'].min()]
}
stats_df = pd.DataFrame(stats, index=['Moyenne', 'Max', 'Min'])

fig2, ax2 = plt.subplots(figsize=(8, 5))

# Palette dégradée de bleu
colors = sns.color_palette("Blues", n_colors=len(stats_df))

stats_df.plot(kind='bar', ax=ax2, color=colors)

ax2.set_title("Comparaison PM10, Température et Humidité")
ax2.set_ylabel("Valeurs")
plt.xticks(rotation=0)

st.pyplot(fig2)


# ----------------------------
# Aperçu des données brutes
# ----------------------------
st.subheader("📄 Aperçu des données brutes")
st.dataframe(df)
