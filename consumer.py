import argparse
import json
import logging
import psycopg2
from confluent_kafka import Consumer

parser = argparse.ArgumentParser()
parser.add_argument("--broker", help="Specify Kafka broker servername:port", required=True)
parser.add_argument("--cacert", help="Specify CA certificate to authenticate to Kafka broker", required=True)
parser.add_argument("--cert", help="Specify certificate to authenticate to Kafka broker", required=True)
parser.add_argument("--certkey", help="Specify certificate key to authenticate to Kafka broker", required=True)
parser.add_argument("--dsn", help="Specify PostgreSQL db connection string", required=True)
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
    logging.info("Open DB connection")
    conn = psycopg2.connect(args.dsn)
    cur = conn.cursor()

    logging.info("Create table for metrics if it doesn't exist")
    cur.execute("CREATE TABLE IF NOT EXISTS metrics (key UUID PRIMARY KEY, value JSONB)")

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
            # This is a happy scenario, we should be getting a message from Kafka
            msg_key = msg.key().decode('utf-8')
            msg_value = msg.value().decode('utf-8')

            logging.info(f"Received message:\nkey: {msg_key}\nvalue: {msg_value}")

            logging.info('Put obtained metrics into DB')
            cur.execute("INSERT INTO metrics(key, value) VALUES(%s, %s)", (msg_key, msg_value))
            conn.commit()
except KeyboardInterrupt:
    # TODO: do multiple except to include (Exception, psycopg2.DatabaseError) as error
    pass
finally:
    # Leave group and commit final offsets
    consumer.close()
    logging.info("Close DB connection")
    cur.close()
    conn.close()