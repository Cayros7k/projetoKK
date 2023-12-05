from kafka import KafkaProducer
from faker import Faker
import json
from time import sleep

# Cria uma instância de KafkaProducer que se conecta ao servidor Kafka na porta 9092.
producer = KafkaProducer(bootstrap_servers='localhost:9092')

# Cria uma instância do Faker para gerar dados aleatórios.
faker = Faker()

# Loop que itera 50 vezes
for _ in range(50):
    # Gera dados aleatórios para serem enviados para o Kafka.
    _data = {
        "first_name": faker.first_name(),
        "city": faker.city(),
        "phone_number": faker.phone_number(),
        "state": faker.state(),
        "id":str(_)
    }

    # Converte os dados gerados para um formato JSON codificado em UTF-8.
    _payload = json.dumps(_data).encode("utf-8")

    # Envia os dados para o tópico 'FirstTopic' no servidor Kafka e guarda a resposta.
    response = producer.send('FirstTopic', _payload)

    print(response)

    # Pausa o loop por 2 segundos antes de enviar a próxima mensagem.
    sleep(2)

