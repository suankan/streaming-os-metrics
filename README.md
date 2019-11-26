# Description

This project goal:

- Gathering OS metrics from any OS.
- Sending OS metrics to Kafka topic.
- Ingesting OS metrics from Kafka topic.
- Storing obtained metrics into Postgres DB.

## Used libs

We use Confluent python lib [confluent_kafka](https://github.com/confluentinc/confluent-kafka-python) because of its performance. Its based on native C lib [librdkafka](https://github.com/edenhill/librdkafka). Quick googling reveals huge performance advantage of it over other Kafka clients for Python. [Example performance comparison here](http://activisiongamescience.github.io/2016/06/15/Kafka-Client-Benchmarking/).

## How to execute unit tests

Please [see the code for details](https://github.com/suankan/streaming-os-metrics/blob/master/metrics_test.py#L10-L25) on what exactly do we test, how and why.

You can execute tests using this example:

```
$ python -m unittest metrics_test.py -v
test_get_methods_return_dict (metrics_test.TestMetrics) ... Testing method get_cpu_freq
Testing method get_cpu_percent
Testing method get_cpu_stats
Testing method get_cpu_times
Testing method get_cpu_times_percent
Testing method get_disk_io_counters
Testing method get_disk_usage
Testing method get_host_info
Testing method get_load_average
Testing method get_net_io_counters
Testing method get_swap_memory
Testing method get_virtual_memory
ok

----------------------------------------------------------------------
Ran 1 test in 0.440s

OK
```

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