try:
    from kafka import KafkaProducer
    from faker import Faker
    import json
    from time import sleep
except Exception as e:
    pass

producer = KafkaProducer(bootstrap_servers='localhost:9092')

faker = Faker()

for _ in range(50):
    _data = {
        "first_name": faker.first_name(),
        "city": faker.city(),
        "phone_number": faker.phone_number(),
        "state": faker.state(),
        "id":str(_)
    }
    _payload = json.dumps(_data).encode("utf-8")
    response = producer.send('FirstTopic', _payload)
    print(response)

    sleep(2)

