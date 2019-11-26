import json
import logging
from confluent_kafka import Consumer

logging.basicConfig(filename='./tmp/consumer.log', filemode='w', format='%(asctime)s - %(message)s', level=logging.INFO)

conf = {
    'bootstrap.servers': "kafka-39b301ca-kansuan-4650.aivencloud.com:14598",
    'group.id': "foo",
    'auto.offset.reset': 'earliest',
    'security.protocol': 'SSL',
    'ssl.ca.location': 'certs/ca.pem',
    'ssl.certificate.location': 'certs/service.cert',
    'ssl.key.location': 'certs/service.key'
}

interval = 2

logging.info(f"Starting Kafka Consumer injesting from broker {conf['bootstrap.servers']} every {interval} seconds")

consumer = Consumer(conf)

topics = ["os-metrics"]
logging.info(f'Subscribing to kafka topics {topics}')
consumer.subscribe(topics)

try:
    while True:
        logging.info(f"Waiting {interval} seconds before next polling Kafka topice")
        msg = consumer.poll(interval)
        if msg is None:
            logging.info(f"Have not received any message within {interval}. Retrying.")
            continue
        elif msg.error():
            logging.info(f"Consumer error: {msg.error()}. Retrying.")
            continue
        else:
            logging.info(f"Received message: key {msg.key().decode('utf-8')}, message value {msg.value().decode('utf-8')}")
except KeyboardInterrupt:
    pass
finally:
    # Leave group and commit final offsets
    consumer.close()
