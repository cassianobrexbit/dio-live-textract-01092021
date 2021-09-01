# Repositório de código para o live coding do dia 01/09/2021

Repositório de código para a live sobre o Amazon Textract da Digital Innovation One

## Recursos AWS utilizados na atividade:

- IAM Role para trigger do Amazon Textract.
- Função Lambda em Python.
- Buckets de entrada e saída de arquivos no S3.

## Desenvolvimento

### Criando um bucket no Amazon S3

- S3 Dashboard -> Create bucket -> Selecionar região -> Nas opções de permissões de ```Block Public Access settings for this bucket``` selecione:
  - Block public access to buckets and objects granted through new public bucket or access point policies
  - Block public and cross-account access to buckets and objects through any public bucket or access point policies
  -> Create bucket.

### Criando o Lambda Trigger do Amazon S3

- AWS Lambda Dashboard -> Create function -> Selecionar ```Use a blueprint``` e pesquisar pelo template ```s3-get-object-python```.
- Inserir o nome da função -> Role name ->  em ```Bucket name``` selecionar o bucket criado anteriormente -> adicionar o sufixo ```.png``` para restringir o tipo dos arquivos que poderão ser processados -> Create function.
- Inserir o código que está na pasta ```src``` deste projeto. Este código irá enviar o arquivo recebido pelo Amazon S3 ao Textract e escrever a resposta em um arquivo .txt com o mesmo nome do arquivo enviado.

### Configurar permissões do IAM para o S3 e o Textract

- Selecionar a função criada -> Configuration -> selecionar a role criada -> Attach policies ->  ```AmazonTextractFullAccess``` e ```AmazonS3FullAccess``` -> Attach Policy

### Adicionando um Lambda Layer personalizado

- Baixar o arquivo .zip na pasta ```src``` -> AWS Lambda -> Layers -> Create layer -> inserir um nome -> Upload a .zip file -> Runtimes Python 3.6 3.7 3.8 3.9 -> Create
- Selecionar a função criada -> Layers -> Add Layer e adicionar o layer boto3 criado anteriormente

### Testando a aplicação

- Realizar o upload de imagens de exemplo da pasta ```img``` e verificar os resultados no bucket S3 criado anteriormente.
