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

### How [producer.py](./producer.py) works

As a first iteration I simply hardcoded all Producer configs into the script:

- Kafka brocker server name and port
- TLS Sertificates for authentication
- Name of Kafka topic to write to

### How to run the producer

1. Specify Aiven TSL certs in the script
2. Specify Aiven Kafka broker server name and port in the script
2. Execute the script:
```
python3 producer.py
```
4. Tail the log to see how it goes:
```
tail -f producer.log
```

TODO: Make the producer script to understand either ENV vars for configuration or cmd params.

## Kafka Consumer to retrieve metrics from Kafka and put them into Postgres DB
TODO