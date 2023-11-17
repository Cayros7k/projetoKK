# VISUALIZAÇÃO EM TEMPO REAL DE GRANDES DADOS COM APACHE KAFKA E KIBANA

# Utilizar o venv:
- python -m venv .venv
- .venv\Scripts\activate -> Windows
- source .venv\bin\activate -> Ubuntu

# Instalar todas as bibliotecas utilizadas:
- pip install -r requirements.txt

# Executar o container do Kafka:
- cd .\kafkaDockerCompose\ -> Acessando a pasta
- docker-compose -f kafka-compose.yml up

# Executar o container do ELK/Kibana:
- cd .\kibanaDockerCompose\ -> Acessando a pasta
- docker-compose -f elk-compose.yml up

# URLs de acesso:
- localhost:5601 -> Kibana
- localhost:9200 -> Elasticsearch
- localhost:9092 -> Kafka