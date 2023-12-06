import base64
import json
import requests

# realizar upload e reconhecimento da imagem no S3
api_url = 'https://fcuysjwzch.execute-api.us-east-1.amazonaws.com/dev/hello'
nome_bucket = 'reconhecimento'
nome_arquivo = 'snike'

with open('local/suaimagem.PNG', 'rb') as file:
    imagem_bytes = file.read()
imagem_base64 = base64.b64encode(imagem_bytes).decode('utf-8')
payload = {
    'file': imagem_base64
}
response = requests.post(api_url, data=json.dumps(payload))
print('Chamada Atual:')
print('Status Code:', response.status_code)
print('Response Body:', response.text)

# Comparação Facial
api_url_compare_faces = 'https://fcuysjwzch.execute-api.us-east-1.amazonaws.com/dev/hello/reconhecimento'
with open('local/suaimagem.PNG', 'rb') as file2:
    imagem_bytes_2 = file2.read()
imagem_base64_2 = base64.b64encode(imagem_bytes_2).decode('utf-8')
payload_compare_faces = {
    'file1': imagem_base64,
    'file2': imagem_base64_2
}
response_compare_faces = requests.post(api_url_compare_faces, data=json.dumps(payload_compare_faces))
print('\nNova Chamada para a Função de Comparação Facial:')
print('Status Code:', response_compare_faces.status_code)
print('Response Body:', response_compare_faces.text)

# Delete
api_url_delete_image = 'https://fcuysjwzch.execute-api.us-east-1.amazonaws.com/dev/hello'
response_delete_image = requests.delete(api_url_delete_image, data=json.dumps({'file': imagem_base64}))
print('\nChamada para Deletar a Imagem:')
print('Status Code:', response_delete_image.status_code)
print('Response Body:', response_delete_image.text)


# Atualizar
api_url_update_image = 'https://fcuysjwzch.execute-api.us-east-1.amazonaws.com/dev/hello'
with open('local/imagem.jpg', 'rb') as file_update:
    imagem_bytes_update = file_update.read()
imagem_base64_update = base64.b64encode(imagem_bytes_update).decode('utf-8')
payload_update_image = {
    'file': imagem_base64_update
}
response_update_image = requests.put(api_url_update_image, data=json.dumps(payload_update_image))
print('\nChamada para Atualizar a Imagem:')
print('Status Code:', response_update_image.status_code)
print('Response Body:', response_update_image.text)



