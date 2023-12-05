from kafka import KafkaConsumer
import json
import requests
import os

# ---------------------------------------------------------
os.environ['KAFKA_TOPIC'] = "FirstTopic"
os.environ['SERVER_END_POINT'] = "http://localhost:9200"
# ---------------------------------------------------------

# Classe para fazer upload de registros para o ElasticSearch a partir do Kafka.
class ElasticSearchKafkaUploadRecord:

    # Inicializa a classe com os dados necessários para fazer o upload.
    def __init__(self, json_data, hash_key, index_name):
        self.hash_key = hash_key  # ---------------> Chave Hash para identificar o registro.
        self.json_data = json_data  # -------------> Dados no formato JSON a serem enviados.
        self.index_name = index_name.lower()  # ---> Nome do índice para o ElasticSearch (convertido para minúsculas).

    # Faz o upload dos registros no cluster do ElasticSearch.
    def upload(self):
        """
        Uploads records on Elastic Search Cluster
        :return
        """
        # Formata a URL para o endpoint do ElasticSearch com o nome do índice e a chave hash.
        URL = "{}/{}/_doc/{}".format(
            os.getenv("SERVER_END_POINT"), self.index_name, self.hash_key
        ) 
        print(URL)

        # Define os cabeçalhos para a requisição HTTP.
        headers = {"Content-Type": "application/json"}

        # Faz uma requisição PUT para enviar os dados JSON para o ElasticSearch
        response = requests.request(
            "PUT", URL, headers=headers, data=json.dumps(self.json_data),
        )
        print(response)

        return {"status": 200, "data": {"message": "record uploaded to Elastic Search"}}

# Função principal para consumir mensagens do Kafka e fazer upload para o ElasticSearch.
def main():

    # Cria um consumidor Kafka para o tópico especificado.
    consumer = KafkaConsumer(os.getenv("KAFKA_TOPIC"))

    # Itera sobre as mensagens recebidas do tópico.
    for msg in consumer:

        # Carrega os dados JSON recebidos na mensagem.
        payload = json.loads(msg.value)

        # Adiciona metadados à carga útil, como informações do tópico, partição, offset, timestamp, etc.
        payload["meta_data"]={
            "topic":msg.topic,
            "partition":msg.partition,
            "offset":msg.offset,
            "timestamp":msg.timestamp,
            "timestamp_type":msg.timestamp_type,
            "key":msg.key,
        }

        # Cria um objeto da classe ElasticSearchKafkaUploadRecord para enviar os dados para o ElasticSearch.
        helper = ElasticSearchKafkaUploadRecord(json_data=payload,
                                                index_name=payload.get("meta_data").get("topic"),
                                                hash_key=payload.get("meta_data").get("offset"),
                                                )
        
        # Chama o método de upload para enviar os dados para o ElasticSearch.
        response = helper.upload()

main()