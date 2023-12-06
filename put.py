import boto3
import json
import base64
from io import BytesIO


def lambda_handler(event, context):
    nome_bucket = 'reconhecimento'
    nome_arquivo = 'imagem.png'

    body = json.loads(event['body'])
    imagem_base64_nova = body['file']
    imagem_bytes_nova = base64.b64decode(imagem_base64_nova)

    s3 = boto3.client('s3')

    # Atualizar a imagem no S3
    try:
        s3.put_object(
            Bucket=nome_bucket,
            Key=nome_arquivo,
            Body=BytesIO(imagem_bytes_nova)
        )

        rekognition = boto3.client('rekognition')

        # Realizar o reconhecimento facial na imagem atualizada
        response_rekognition = rekognition.detect_faces(
            Image={'S3Object': {'Bucket': nome_bucket, 'Name': nome_arquivo}}
        )

        # Extrair informações relevantes do resultado do reconhecimento facial
        face_details = []
        for face in response_rekognition['FaceDetails']:
            age_range = face.get('AgeRange', {})
            smile_value = face.get('Smile', {}).get('Value', 'N/A')

            face_details.append({
                'BoundingBox': face['BoundingBox'],
                'AgeRange': age_range,
                'Smile': smile_value,

            })

        return {
            'statusCode': 200,
            'body': json.dumps(
                {'message': f"Imagem {nome_arquivo} atualizada com sucesso e reconhecimento facial concluído.",
                 'face_details': face_details})
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': f"Erro ao atualizar a imagem ou realizar o reconhecimento facial: {str(e)}"})
        }
