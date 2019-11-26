# Description

This project goal:

- Gathering OS metrics from any OS.
- Sending OS metrics to Kafka topic.
- Ingesting OS metrics from Kafka topic.
- Storing obtained metrics into Postgres DB.

## Used libs

We use Confluent python lib [confluent_kafka](https://github.com/confluentinc/confluent-kafka-python) because of its performance. Its based on native C lib [librdkafka](https://github.com/edenhill/librdkafka). Quick googling reveals huge performance advantage of it over other Kafka clients for Python. [Example performance comparison here](http://activisiongamescience.github.io/2016/06/15/Kafka-Client-Benchmarking/).

## Gathering OS metrics via class `Metrics`

Gathering OS runtime metrics for CPU, Memory and Disks in JSON format is implemented via module [metrics.py](./metrics.py)

## How to execute Kafka Producer

Put `metrics.py` and `producer.py` on the server which you want to monitor.

Execute the script with specifying the Kafka broker server:port, TLS certificates and interval.

This script will be:
- taking OS metrics using class `Metrics`
- sending them to Kafka topic

```
python producer.py --broker kafka-39b301ca-kansuan-4650.aivencloud.com:14598 --cacert certs/ca.pem --cert certs/service.cert --certkey certs/service.key  --interval 2
```

Tail the log to see how it goes:
```
tail -f ./tmp/producer.log
```

## How to execute Kafka Consumer

Execute the script with specifying the Kafka broker server:port, TLS certificates and interval.

```
python consumer.py --broker kafka-39b301ca-kansuan-4650.aivencloud.com:14598 --cacert certs/ca.pem --cert certs/service.cert --certkey certs/service.key --interval 2
```

Tail the log to see how it goes:
```
tail -f ./tmp/consumer.log
```

TODO: put obtained metrics into Postgres DB.