import argparse
import json
import logging
from confluent_kafka import Consumer

parser = argparse.ArgumentParser()
parser.add_argument("--broker", help="Specify Kafka broker servername:port", required=True)
parser.add_argument("--cacert", help="Specify CA certificate to authenticate to Kafka broker", required=True)
parser.add_argument("--cert", help="Specify certificate to authenticate to Kafka broker", required=True)
parser.add_argument("--certkey", help="Specify certificate key to authenticate to Kafka broker", required=True)
parser.add_argument("--topic", help="Specify Kafka topic to write metrics to. Defaults to os-metrics", default="os-metrics")
parser.add_argument("--interval", help="Specify polling interval for gathering metrics. Defaults to 2 sec", default=2)
parser.add_argument("--log", help="Specify log file. Defaults to ./tmp/consumer.log", default='./tmp/consumer.log')
args = parser.parse_args()

conf = {
    'bootstrap.servers': args.broker,
    'group.id': "foo",
    'auto.offset.reset': 'earliest',
    'security.protocol': 'SSL',
    'ssl.ca.location': args.cacert,
    'ssl.certificate.location': args.cert,
    'ssl.key.location': args.certkey
}

logging.basicConfig(filename=args.log, filemode='w', format='%(asctime)s - %(message)s', level=logging.INFO)

logging.info(f"Starting Kafka Consumer injesting from broker {conf['bootstrap.servers']} every {args.interval} seconds")
consumer = Consumer(conf)

logging.info(f'Subscribing to kafka topic {args.topic}')
consumer.subscribe([args.topic])

try:
    while True:
        logging.info(f"Setting polling interval {args.interval} seconds to read from Kafka topic.")
        msg = consumer.poll(int(args.interval))
        if msg is None:
            logging.info(f"Have not received any message within {args.interval}. Retrying.")
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
