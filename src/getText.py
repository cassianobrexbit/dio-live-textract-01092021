import json
import boto3
import os
import urllib.parse

print('Loading function')

s3 = boto3.client('s3')

# Amazon Textract client
textract = boto3.client('textract')

def getTextractData(bucketName, documentKey):
    print('Loading getTextractData')
    # Call Amazon Textract
    response = textract.detect_document_text(
        Document={
            'S3Object': {
                'Bucket': bucketName,
                'Name': documentKey
            }
        })
        
    detectedText = ''

    # Print detected text
    for item in response['Blocks']:
        if item['BlockType'] == 'LINE':
            detectedText += item['Text'] + '\n'
            
    return detectedText
    
def writeTextractToS3File(textractData, bucketName, createdS3Document):
    print('Loading writeTextractToS3File')
    generateFilePath = os.path.splitext(createdS3Document)[0] + '.txt'
    s3.put_object(Body=textractData, Bucket=bucketName, Key=generateFilePath)
    print('Generated ' + generateFilePath)
    

def lambda_handler(event, context):
    # Get the object from the event and show its content type
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'], encoding='utf-8')
    try:
        detectedText = getTextractData(bucket, key)
        writeTextractToS3File(detectedText, bucket, key)
        
        return 'Processing Done!'

    except Exception as e:
        print(e)
        print('Error getting object {} from bucket {}. Make sure they exist and your bucket is in the same region as this function.'.format(key, bucket))
        raise e
