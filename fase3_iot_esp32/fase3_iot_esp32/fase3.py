import sqlite3
import random
from datetime import datetime
import pandas as pd

from fase5_aws.alertas import enviar_alerta


# usa exatamente o nome do arquivo que está no GitHub
CAMINHO_BANCO = "fase3_iot_esp32/farmtech (1).db"


def conectar_banco():
    """
    Abre conexão com o banco SQLite da Fase 3.
    """
    conn = sqlite3.connect(CAMINHO_BANCO)
    return conn


def simular_leitura_sensores(talhao_id: int) -> dict:
    """
    Simula uma leitura de sensores para um talhão.
    Valores aleatórios, apenas para testes.
    """
    leitura = {
        "talhao_id": talhao_id,
            "data_hora": datetime.now().isoformat(sep=" ", timespec="seconds"),
        "umidade": round(random.uniform(10, 80), 1),
        "ph": round(random.uniform(4.5, 7.5), 1),
        "nutrientes": round(random.uniform(20, 100), 1),
        "origem": "simulado",
    }
    return leitura


def garantir_tabela_leituras(conn):
    """
    Garante que a tabela leituras_sensores exista.
    (caso tenha sido criada na Fase 2, este comando só confirma)
    """
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS leituras_sensores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            talhao_id INTEGER,
            data_hora TEXT,
            umidade REAL,
            ph REAL,
            nutrientes REAL,
            origem TEXT
        );
        """
    )
    conn.commit()


def inserir_leitura_no_banco(conn, leitura: dict):
    """
    Insere uma leitura de sensores na tabela leituras_sensores.
    """
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO leituras_sensores
        (talhao_id, data_hora, umidade, ph, nutrientes, origem)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            leitura["talhao_id"],
            leitura["data_hora"],
            leitura["umidade"],
            leitura["ph"],
            leitura["nutrientes"],
            leitura["origem"],
        ),
    )
    conn.commit()


def avaliar_irrigacao_e_alertar(leitura: dict) -> str:
    """
    Regra simples de automação:
    - Se umidade < 30 -> ligar bomba e disparar alerta AWS SNS
    - Senão -> não ligar bomba

    Retorna a ação tomada (string).
    """
    umidade = leitura["umidade"]

    if umidade < 30:
        acao = "LIGAR BOMBA por 15 minutos"

        mensagem = (
            f"Alerta de umidade baixa na FarmTech!\n\n"
            f"Talhão: {leitura['talhao_id']}\n"
            f"Data/hora: {leitura['data_hora']}\n"
            f"Umidade: {leitura['umidade']}%\n"
            f"pH: {leitura['ph']}\n"
            f"Nutrientes: {leitura['nutrientes']}\n\n"
            f"Ação sugerida: {acao}."
        )

        try:
            enviar_alerta(
                mensagem,
                assunto=f"Alerta de Umidade - Talhão {leitura['talhao_id']}",
            )
        except Exception as e:
            # Para não quebrar o sistema caso a AWS falhe
            print("Falha ao enviar alerta AWS:", e)

    else:
        acao = "NÃO ligar bomba (umidade suficiente)"

    return acao


def rodar_ciclo_leitura(talhao_id: int = 1) -> dict:
    """
    Executa um ciclo completo:
    - conecta no banco
    - garante tabela
    - simula leitura
    - insere no banco
    - avalia irrigação e dispara alerta (se preciso)
    - retorna um dicionário com leitura + ação
    """
    conn = conectar_banco()
    garantir_tabela_leituras(conn)

    leitura = simular_leitura_sensores(talhao_id)
    inserir_leitura_no_banco(conn, leitura)
    acao = avaliar_irrigacao_e_alertar(leitura)

    conn.close()

    retorno = leitura.copy()
    retorno["acao"] = acao
    return retorno


def obter_ultimas_leituras(qtd: int = 10) -> pd.DataFrame:
    """
    Retorna as últimas leituras da tabela leituras_sensores.
    Útil para mostrar na dashboard.
    """
    conn = conectar_banco()
    df = pd.read_sql_query(
        f"SELECT * FROM leituras_sensores ORDER BY id DESC LIMIT {qtd};",
        conn,
    )
    conn.close()
    return df


if __name__ == "__main__":
    # Teste rápido de ciclo com talhão 1
    resultado = rodar_ciclo_leitura(talhao_id=1)
    print("Resultado do ciclo:", resultado)

    print("\nÚltimas leituras:")
    print(obter_ultimas_leituras(5))
