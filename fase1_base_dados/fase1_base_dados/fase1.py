import pandas as pd
import requests


def criar_base_talhoes():
    """
    Cria a base inicial de talhões e culturas.
    (mesmos dados do notebook)
    """
    dados_talhoes = {
        "talhao_id": [1, 2, 3],
        "cultura": ["Soja", "Milho", "Cana"],
        "comprimento_m": [100, 150, 200],
        "largura_m": [50, 80, 120],
    }
    df = pd.DataFrame(dados_talhoes)
    return df


def calcular_area_e_insumos(df_talhoes: pd.DataFrame) -> pd.DataFrame:
    """
    Calcula área (m² e ha) e fertilizante necessário por talhão.
    """
    # Área
    df_talhoes["area_m2"] = df_talhoes["comprimento_m"] * df_talhoes["largura_m"]
    df_talhoes["area_ha"] = df_talhoes["area_m2"] / 10_000

    # Dose de fertilizante (kg/ha) por cultura
    fertilizante_por_cultura = {
        "Soja": 50,
        "Milho": 70,
        "Cana": 90,
    }

    def calcula_fertilizante(cultura, area_ha):
        dose_ha = fertilizante_por_cultura.get(cultura, 50)
        return dose_ha * area_ha

    df_talhoes["fertilizante_kg"] = df_talhoes.apply(
        lambda row: calcula_fertilizante(row["cultura"], row["area_ha"]),
        axis=1,
    )

    return df_talhoes


def integrar_meteorologia(
    df_talhoes: pd.DataFrame,
    latitude: float = -22.5,
    longitude: float = -47.5,
) -> pd.DataFrame:
    """
    Consulta API pública de meteorologia (Open-Meteo),
    calcula temperatura média e chuva total dos últimos 7 dias
    e adiciona essas infos em todos os talhões.
    """
    url = (
        "https://api.open-meteo.com/v1/forecast"
        "?latitude={lat}&longitude={lon}"
        "&hourly=temperature_2m,precipitation"
        "&past_days=7"
        "&timezone=auto"
    ).format(lat=latitude, lon=longitude)

    response = requests.get(url)
    dados_meteo = response.json()

    horas = dados_meteo["hourly"]["time"]
    temperaturas = dados_meteo["hourly"]["temperature_2m"]
    chuvas = dados_meteo["hourly"]["precipitation"]

    df_meteo_horario = pd.DataFrame(
        {
            "time": pd.to_datetime(horas),
            "temperatura_C": temperaturas,
            "chuva_mm": chuvas,
        }
    )

    df_meteo_diario = (
        df_meteo_horario.set_index("time")
        .resample("D")
        .agg({"temperatura_C": "mean", "chuva_mm": "sum"})
        .reset_index()
    )

    temp_media_7d = df_meteo_diario["temperatura_C"].mean()
    chuva_total_7d = df_meteo_diario["chuva_mm"].sum()

    def recomenda_irrigacao(chuva_total_7d):
        if chuva_total_7d < 10:
            return "Alta prioridade de irrigação"
        elif chuva_total_7d < 30:
            return "Monitorar irrigação"
        else:
            return "Irrigação reduzida"

    df_talhoes["temp_media_7d"] = temp_media_7d
    df_talhoes["chuva_total_7d"] = chuva_total_7d
    df_talhoes["recomendacao_irrigacao"] = recomenda_irrigacao(chuva_total_7d)

    return df_talhoes


def salvar_bases(df_talhoes: pd.DataFrame):
    """
    Salva as bases da Fase 1 na pasta local do projeto.
    (na Fase 7 você pode reaproveitar ou adaptar)
    """
    df_sem_meteo = df_talhoes.drop(
        columns=["temp_media_7d", "chuva_total_7d", "recomendacao_irrigacao"],
        errors="ignore",
    )
    df_sem_meteo.to_csv("base_fase1_talhoes_insumos.csv", index=False)
    df_talhoes.to_csv("base_fase1_com_meteo.csv", index=False)


if __name__ == "__main__":
    # Pipeline completo da Fase 1: gera os dados do zero
    df = criar_base_talhoes()
    df = calcular_area_e_insumos(df)
    df = integrar_meteorologia(df)

    salvar_bases(df)

    print("Bases da Fase 1 geradas com sucesso.")
    print(df)
