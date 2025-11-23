import os
import pandas as pd
from fase5_aws.alertas import enviar_alerta

# Caminho do CSV gerado no notebook da Fase 6
CAMINHO_CSV = "fase6_visao_computacional/fase6_resultados_visao.csv"


def carregar_resultados() -> pd.DataFrame:
    """
    Carrega o CSV gerado na Fase 6 com o resumo da visão computacional.
    """
    if not os.path.exists(CAMINHO_CSV):
        raise FileNotFoundError(
            f"Arquivo de resultados da Fase 6 não encontrado: {CAMINHO_CSV}"
        )

    df = pd.read_csv(CAMINHO_CSV)
    return df


def analisar_e_alertar() -> pd.DataFrame:
    """
    Lê os resultados da visão computacional e, se houver imagens
    com objetos_detectados > 0, dispara um alerta via AWS SNS.

    Retorna o DataFrame completo para exibição na dashboard.
    """
    df = carregar_resultados()

    # Imagens com algum objeto detectado
    problemas = df[df["objetos_detectados"] > 0]

    if not problemas.empty:
        mensagem = "Alerta de Visão Computacional na FarmTech!\n\n"

        for _, row in problemas.iterrows():
            mensagem += (
                f"Imagem: {row['imagem']}\n"
                f"Objetos detectados: {row['objetos_detectados']}\n"
                f"Classes: {row['classes_detectadas']}\n\n"
            )

        mensagem += "Ação sugerida: inspecionar as áreas correspondentes."

        try:
            enviar_alerta(mensagem, assunto="Alerta Visão Computacional - FarmTech")
        except Exception as e:
            # Não quebrar o sistema se a AWS falhar
            print("Falha ao enviar alerta AWS (Fase 6):", e)

    return df


if __name__ == "__main__":
    # Teste rápido se você rodar esse arquivo sozinho (python fase6.py)
    try:
        df_teste = analisar_e_alertar()
        print(df_teste)
    except Exception as e:
        print("Erro ao analisar Fase 6:", e)
