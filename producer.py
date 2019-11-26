import logging
import time
import uuid
from metrics import Metrics
from confluent_kafka import Producer

def delivery_report(err, msg):
    '''
    Called once for each message produced to indicate delivery result.
    Triggered by poll() or flush().
    '''
    if err is not None:
        logging.info(f'Message delivery failed: {err}')
    else:
        logging.info(f'Message delivered to {msg.topic()} partition {msg.partition()}')

def run_producer(p, interval):
    try:
        while True:
            logging.info(f'Sleeping {interval} seconds before next metrics collection')
            time.sleep(interval)

            logging.info(f'Collecting metrics')
            metrics = Metrics()

            key = str(uuid.uuid4())
            topic = "os-metrics"
            logging.info(f'Sending metrics to Kafka topic {topic}, key {key}')
            p.produce(topic, key=str(key), value=metrics.to_json(), callback=delivery_report)

            logging.info(f'Wait for all messages in the Producer queue to be delivered.')
            p.flush()
    except KeyboardInterrupt:
        pass

logging.basicConfig(filename='producer.log', filemode='w', format='%(asctime)s - %(message)s', level=logging.INFO)

p = Producer({
    'bootstrap.servers': 'kafka-39b301ca-kansuan-4650.aivencloud.com:14598',
    'client.id': 'test',
    'default.topic.config': {'acks': 'all'},

    'security.protocol': 'SSL',
    'ssl.ca.location': 'certs/ca.pem',
    'ssl.certificate.location': 'certs/service.cert',
    'ssl.key.location': 'certs/service.key'
})

run_producer(p, 2)
