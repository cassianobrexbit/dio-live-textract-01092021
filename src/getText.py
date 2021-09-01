import json
import boto3
import os
import urllib.parse

s3 = boto3.client('s3')

# Cliente do Amazon Textract
textract = boto3.client('textract')

def getTextractData(bucketName, documentKey):
    
    # Chamando o Amazon Textract com os parâmetros do bucket e do arquivo .png
    response = textract.detect_document_text(
        Document={
            'S3Object': {
                'Bucket': bucketName,
                'Name': documentKey
            }
        })
        
    detectedText = ''

    # Imprime o texto obtido da imagem
    # Um obketo do tipo Block representa o item reconhecido em um documento com pixels próximos uns aos outros
    for item in response['Blocks']:
        if item['BlockType'] == 'LINE':
            detectedText += item['Text'] + '\n'
            
    return detectedText
    
# Escreve os resultados em um arquivo .txt
def writeTextractToS3File(textractData, bucketName, createdS3Document):
    print('Loading writeTextractToS3File')
    generateFilePath = os.path.splitext(createdS3Document)[0] + '.txt'
    s3.put_object(Body=textractData, Bucket=bucketName, Key=generateFilePath)
    print('Generated ' + generateFilePath)
    

def lambda_handler(event, context):
    # Obtém o objeto (arquivo) após o trigger o Amazon S3 ser disparado com o upload.
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'], encoding='utf-8')
    try:
        detectedText = getTextractData(bucket, key)
        writeTextractToS3File(detectedText, bucket, key)
        
        return 'Concluído!'

    except Exception as e:
        print(e)
        print('Erro ao obter objeto {} do bucket {}.'.format(key, bucket))
        raise e
