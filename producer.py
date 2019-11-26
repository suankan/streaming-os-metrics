import logging
import time
import uuid
import argparse
import sys
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

parser = argparse.ArgumentParser()
parser.add_argument("--broker", help="Specify Kafka broker servername:port")
parser.add_argument("--cacert", help="Specify CA certificate to authenticate to Kafka broker")
parser.add_argument("--cert", help="Specify certificate to authenticate to Kafka broker")
parser.add_argument("--certkey", help="Specify certificate key to authenticate to Kafka broker")
parser.add_argument("--topic", help="Specify Kafka topic to write metrics to. Defaults to os-metrics", default="os-metrics")
parser.add_argument("--interval", help="Specify polling interval for gathering metrics. Defaults to 2 sec", default=2)
parser.add_argument("--log", help="Specify log file. Defaults to ./tmp/producer.log", default='./tmp/producer.log')
args = parser.parse_args()

if not args.broker or not args.cacert or not args.cert or not args.certkey:
    print(f'You must specify --broker, --cacert, --cert, --certkey options to this command')
    exit(1)

logging.basicConfig(stream=sys.stdout, filemode='w', format='%(asctime)s - %(message)s', level=logging.INFO)

p = Producer({
    'bootstrap.servers': args.broker,
    'client.id': 'test',
    'default.topic.config': {'acks': 'all'},
    'security.protocol': 'SSL',
    'ssl.ca.location': args.cacert,
    'ssl.certificate.location': args.cert,
    'ssl.key.location': args.certkey
})

try:
    while True:
        logging.info(f'Sleeping {args.interval} seconds before next metrics collection')
        time.sleep(int(args.interval))

        logging.info(f'Collecting metrics')
        metrics = Metrics()

        key = str(uuid.uuid4())
        logging.info(f'Sending metrics to Kafka broker {args.broker} topic {args.topic}, key {key}')
        p.produce(args.topic, key=str(key), value=metrics.to_json(), callback=delivery_report)

        logging.info(f'Wait for all messages in the Producer queue to be delivered.')
        p.flush()
except KeyboardInterrupt:
    pass
