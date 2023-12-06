
import json
import boto3
import botocore.exceptions
import base64
from io import BytesIO

rekognition = boto3.client('rekognition')

def lambda_handler(event, context):
    try:

        body = json.loads(event['body'])
        imagem_base64_1 = body['file1']
        imagem_base64_2 = body['file2']

        imagem_bytes_1 = base64.b64decode(imagem_base64_1)
        imagem_bytes_2 = base64.b64decode(imagem_base64_2)

        # Realizar o reconhecimento facial nas duas imagens
        response_rekognition_1 = rekognition.detect_faces(Image={'Bytes': imagem_bytes_1})
        response_rekognition_2 = rekognition.detect_faces(Image={'Bytes': imagem_bytes_2})

        # Verificar se há faces nas duas imagens
        if not response_rekognition_1['FaceDetails'] or not response_rekognition_2['FaceDetails']:
            return {
                'statusCode': 200,
                'body': json.dumps({'is_same_person': False, 'message': 'Uma ou ambas as imagens não contêm rostos.'})
            }

        # Comparar as faces nas duas imagens
        similarity_threshold = 70  # Ajuste conforme necessário
        response_similarity = rekognition.compare_faces(
            SourceImage={'Bytes': imagem_bytes_1},
            TargetImage={'Bytes': imagem_bytes_2},
            SimilarityThreshold=similarity_threshold
        )

        is_same_person = len(response_similarity['FaceMatches']) > 0


        return {
            'statusCode': 200,
            'body': json.dumps({'is_same_person': is_same_person})
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
