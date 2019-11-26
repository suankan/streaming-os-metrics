# Streaming OS metrics to Postresql via Kafka

## Gathering OS metrics

Gather OS runtime metrics for CPU, Memory and Disks in JSON format.

Implemented via module [metrics.py](./metrics.py)

### How to use the Class Metrics

This is pretty much a wrapper around python psutil library functions.
The only customisation is that we gather info about all CPUs instead combined CPU stats.

Instantiate the class and constructor will actually run gathering the stats.
Then use `.to_json()` method to get the stats in a JSON format.

## Kafka Producer to send metrics to Kafka

We use Confluent python lib [confluent_kafka](https://github.com/confluentinc/confluent-kafka-python) because of its performance. Its based on native C lib [librdkafka](https://github.com/edenhill/librdkafka). Quick googling reveals huge performance advantage of it over other Kafka clients for Python. [Example performance comparison here](http://activisiongamescience.github.io/2016/06/15/Kafka-Client-Benchmarking/).

### How to run producer

Execute the script with specifying the Kafka broker server:port and TLS certificates.
```
python producer.py --broker kafka-39b301ca-kansuan-4650.aivencloud.com:14598 --cacert certs/ca.pem --cert certs/service.cert --certkey certs/service.key  --interval 2
```

Tail the log to see how it goes:
```
tail -f ./tmp/producer.log
```

## Kafka Consumer to retrieve metrics from Kafka and put them into Postgres DB

Execute the script with specifying the Kafka broker server:port and TLS certificates.
```
python consumer.py --broker kafka-39b301ca-kansuan-4650.aivencloud.com:14598 --cacert certs/ca.pem --cert certs/service.cert --certkey certs/service.key --interval 2
```

Tail the log to see how it goes:
```
tail -f ./tmp/consumer.log
```
