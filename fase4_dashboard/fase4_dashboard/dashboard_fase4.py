import streamlit as st
import pandas as pd
from sklearn.ensemble import RandomForestRegressor

# Carrega dados da Fase 1 (ajuste o caminho se precisar)
df = pd.read_csv("fase1_base_dados/base_fase1_com_meteo.csv")

# Cria variável de produtividade (mesma lógica do notebook)
df["produtividade_sacas_ha"] = (
    40
    + df["fertilizante_kg"] * 0.2
    - (df["temp_media_7d"] - 22) * 1.5
    + (df["chuva_total_7d"] * 0.3)
)

X = df[["area_ha", "fertilizante_kg", "temp_media_7d", "chuva_total_7d"]]
y = df["produtividade_sacas_ha"]

modelo = RandomForestRegressor(random_state=42)
modelo.fit(X, y)


def prever_produtividade(area_ha, fertilizante_kg, temp_media, chuva_total):
    entrada = pd.DataFrame(
        [
            {
                "area_ha": area_ha,
                "fertilizante_kg": fertilizante_kg,
                "temp_media_7d": temp_media,
                "chuva_total_7d": chuva_total,
            }
        ]
    )
    pred = modelo.predict(entrada)[0]
    return round(pred, 2)


def main():
    st.title("Dashboard FarmTech - Fase 4")
    st.write("Visualização dos talhões e previsão de produtividade.")

    st.subheader("Dados atuais da fazenda")
    st.dataframe(df)

    st.subheader("Simular produtividade esperada")

    area_ha = st.number_input(
        "Área (ha)", min_value=0.1, value=float(df["area_ha"].iloc[0])
    )
    fertilizante_kg = st.number_input(
        "Fertilizante (kg)",
        min_value=0.0,
        value=float(df["fertilizante_kg"].iloc[0]),
    )
    temp_media = st.number_input(
        "Temperatura média 7 dias (°C)", value=float(df["temp_media_7d"].iloc[0])
    )
    chuva_total = st.number_input(
        "Chuva total 7 dias (mm)", value=float(df["chuva_total_7d"].iloc[0])
    )

    if st.button("Prever produtividade"):
        prod = prever_produtividade(area_ha, fertilizante_kg, temp_media, chuva_total)
        st.success(f"Produtividade estimada: {prod} sacas/ha")


if __name__ == "__main__":
    main()
