import os
import boto3


# ⚠️ IMPORTANTE:
# NÃO coloque suas chaves reais aqui dentro.
# Use variáveis de ambiente (ou o arquivo de credenciais da AWS).
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_REGION = os.getenv("AWS_REGION", "us-east-1")
SNS_TOPIC_ARN = os.getenv("SNS_TOPIC_ARN")  # cole o ARN numa env var


def enviar_alerta(mensagem: str, assunto: str = "Alerta FarmTech"):
    """
    Envia um alerta para um tópico SNS na AWS.
    Essa função será usada pela Fase 3 e pela dashboard final.
    """
    if not SNS_TOPIC_ARN:
        raise ValueError("SNS_TOPIC_ARN não configurado nas variáveis de ambiente.")

    client = boto3.client(
        "sns",
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        region_name=AWS_REGION,
    )

    response = client.publish(
        TopicArn=SNS_TOPIC_ARN,
        Message=mensagem,
        Subject=assunto,
    )

    return response


if __name__ == "__main__":
    # Teste simples (só roda se você executar esse arquivo diretamente)
    msg_teste = "Teste de alerta FarmTech enviado a partir do script alertas.py."
    print("Enviando mensagem de teste...")
    resp = enviar_alerta(msg_teste, assunto="Teste - FarmTech")
    print("Resposta da AWS SNS:", resp)
