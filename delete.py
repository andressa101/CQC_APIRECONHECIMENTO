import boto3
import json


def lambda_handler(event, context):
    nome_bucket = 'reconhecimento'
    nome_arquivo = 'imagem.png'

    s3 = boto3.client('s3')

    # Deletar o objeto (imagem) do bucket
    try:
        response = s3.delete_object(Bucket=nome_bucket, Key=nome_arquivo)
        return {
            'statusCode': 200,
            'body': json.dumps({'message': f"Imagem {nome_arquivo} deletada com sucesso do bucket {nome_bucket}"})
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': f"Erro ao deletar a imagem: {str(e)}"})
        }
