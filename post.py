import json
import boto3
import botocore.exceptions
import base64
from io import BytesIO

rekognition = boto3.client('rekognition')
s3 = boto3.client('s3')


def lambda_handler(event, context):
    try:

        body = json.loads(event['body'])
        imagem_base64 = body['file']
        imagem_bytes = base64.b64decode(imagem_base64)

        # Salvar a imagem no Amazon S3
        bucket_name = 'reconhecimento'
        nome_arquivo_s3 = 'imagem.png'

        s3.upload_fileobj(
            BytesIO(imagem_bytes),
            bucket_name,
            nome_arquivo_s3
        )

        # Realizar o reconhecimento facial
        response_rekognition = rekognition.detect_faces(
            Image={'S3Object': {'Bucket': bucket_name, 'Name': nome_arquivo_s3}})

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
            'body': json.dumps({'face_details': face_details})
        }

    except botocore.exceptions.NoCredentialsError:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': 'As credenciais da AWS não foram encontradas.'})
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
