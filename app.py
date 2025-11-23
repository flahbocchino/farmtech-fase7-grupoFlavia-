import streamlit as st
import pandas as pd

from fase3_iot_esp32.fase3 import rodar_ciclo_leitura, obter_ultimas_leituras
from fase6_visao_computacional.fase6 import carregar_resultados, analisar_e_alertar


# ==========================
# Funções auxiliares – Fase 1
# ==========================

@st.cache_data
def carregar_bases_fase1():
    """Carrega as bases da Fase 1 (talhões/insumos e meteorologia)."""
    df_talhoes = pd.read_csv(
        "fase1_base_dados/base_fase1_talhoes_insumos.csv"
    )
    df_meteo = pd.read_csv(
        "fase1_base_dados/base_fase1_com_meteo.csv"
    )

    # Garante cálculo de área
    if "area_m2" not in df_talhoes.columns:
        if {"comprimento_m", "largura_m"}.issubset(df_talhoes.columns):
            df_talhoes["area_m2"] = (
                df_talhoes["comprimento_m"] * df_talhoes["largura_m"]
            )

    df_talhoes["area_ha"] = df_talhoes["area_m2"] / 10_000
    return df_talhoes, df_meteo


# ==========================
# Páginas da dashboard
# ==========================

def pagina_visao_geral():
    st.title("FarmTech – Dashboard Integrada (Fase 7)")
    st.write(
        """
        Esta dashboard consolida as Fases 1, 3, 4, 5 e 6 em um único sistema.
        Use o menu lateral para navegar entre as funcionalidades.
        """
    )

    df_talhoes, df_meteo = carregar_bases_fase1()
    df_visao = carregar_resultados()

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Número de talhões", len(df_talhoes))
    with col2:
        st.metric("Área total (ha)", round(df_talhoes["area_ha"].sum(), 2))
    with col3:
        st.metric(
            "Imagens com possíveis problemas",
            int((df_visao["objetos_detectados"] > 0).sum()),
        )

    st.subheader("Talhões cadastrados (Fase 1)")
    st.dataframe(df_talhoes)

    st.subheader("Resumo meteorológico (Fase 1)")
    st.dataframe(df_meteo.head())


def pagina_fase1():
    st.title("Fase 1 – Base de Dados da Fazenda")

    df_talhoes, df_meteo = carregar_bases_fase1()

    st.subheader("Talhões, insumos e área calculada")
    st.dataframe(df_talhoes)

    st.subheader("Meteorologia integrada")
    st.dataframe(df_meteo)

    st.info(
        "Esses dados vêm da Fase 1 e alimentam as demais fases (banco, IoT e previsões)."
    )


def pagina_fase3():
    st.title("Fase 3 – IoT, Sensores e Irrigação Automática")

    st.write(
        """
        Aqui simulamos uma leitura de sensores (ESP32) e registramos no banco.
        Se a umidade estiver baixa, um alerta é enviado via AWS SNS (Fase 5).
        """
    )

    talhao_id = st.number_input(
        "Talhão para leitura simulada:",
        min_value=1,
        value=1,
        step=1,
    )

    if st.button("Capturar leitura agora"):
        resultado = rodar_ciclo_leitura(talhao_id=int(talhao_id))
        st.success("Leitura registrada com sucesso!")
        st.json(resultado)

    st.subheader("Últimas leituras registradas")
    try:
        df_ultimas = obter_ultimas_leituras(20)
        st.dataframe(df_ultimas)
    except Exception as e:
        st.error(f"Não foi possível carregar as leituras de sensores: {e}")


def pagina_fase4():
    st.title("Fase 4 – Dashboard de Produtividade (resumo)")

    df_talhoes, df_meteo = carregar_bases_fase1()

    st.write(
        """
        A Fase 4 original implementa um modelo de Machine Learning em Streamlit.
        Aqui apresentamos um resumo simples com base nas mesmas informações,
        simulando uma 'produtividade estimada' proporcional à área e a um
        índice climático.
        """
    )

    # Exemplo simples de "índice de produtividade"
    df_talhoes["produtividade_estimada"] = (
        df_talhoes["area_ha"] * 3.5  # coeficiente arbitrário apenas para demo
    )

    st.subheader("Produtividade estimada por talhão (exemplo)")
    st.dataframe(
        df_talhoes[["talhao_id", "cultura", "area_ha", "produtividade_estimada"]]
    )

    st.info(
        "Para detalhes completos da Fase 4, consulte o arquivo "
        "`fase4_dashboard/dashboard_fase4.py` no repositório."
    )


def pagina_fase6():
    st.title("Fase 6 – Visão Computacional da Lavoura")

    st.write(
        """
        Esta página usa os resultados gerados na Fase 6. Os dados estão em
        `fase6_visao_computacional/fase6_resultados_visao.csv`. A partir deles,
        podemos visualizar quais imagens possuem possíveis problemas e,
        opcionalmente, disparar alertas via AWS SNS.
        """
    )

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Apenas carregar resultados"):
            df_visao = carregar_resultados()
            st.session_state["df_visao"] = df_visao
    with col2:
        if st.button("Rodar análise e enviar alertas"):
            df_visao = analisar_e_alertar()
            st.session_state["df_visao"] = df_visao
            st.success("Análise executada. Se configurado, alerta enviado via AWS.")

    df_visao = st.session_state.get("df_visao", None)
    if df_visao is not None:
        st.subheader("Resultados da visão computacional")
        st.dataframe(df_visao)
    else:
        st.info("Clique em um dos botões acima para carregar os resultados.")


# ==========================
# Função principal
# ==========================

def main():
    st.set_page_config(
        page_title="FarmTech – Fase 7",
        layout="wide",
    )

    menu = st.sidebar.radio(
        "Navegação",
        [
            "Visão geral",
            "Fase 1 – Base de Dados",
            "Fase 3 – Sensores & Irrigação",
            "Fase 4 – Produtividade (resumo)",
            "Fase 6 – Visão Computacional",
        ],
    )

    if menu == "Visão geral":
        pagina_visao_geral()
    elif menu == "Fase 1 – Base de Dados":
        pagina_fase1()
    elif menu == "Fase 3 – Sensores & Irrigação":
        pagina_fase3()
    elif menu == "Fase 4 – Produtividade (resumo)":
        pagina_fase4()
    elif menu == "Fase 6 – Visão Computacional":
        pagina_fase6()


if __name__ == "__main__":
    main()
