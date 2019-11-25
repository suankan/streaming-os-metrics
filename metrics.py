'''
This is a module with classes implementing gathering OS metrics.
'''

import time
import psutil
import json
import platform

class Metrics():
    '''
    This class gets OS Metrics and sends them to Kafka.
    Metrics are obtained using psutil lib.
    More info: https://psutil.readthedocs.io/en/latest/#psutil-documentation
    '''
    def __init__(self):
        # Create a list of CPUs like ['cpu1', 'cpu2', ... , 'cpuN']
        self.list_cpus = ['cpu' + str(item) for item in range(psutil.cpu_count(logical=True))]

        self.metrics = {
                'snapshot_started': time.time(),
            'host_info': self.get_host_info(),
                'cpu_times': self.get_cpu_times(),
                'cpu_percent': self.get_cpu_percent(),
                'cpu_times_percent': self.get_cpu_times_percent(),
                'cpu_stats': self.get_cpu_stats(),
                'cpu_freq': self.get_cpu_freq(),
                'load_average': self.get_load_average(),
                'snapshot_finished': time.time()
            }

    def get_host_info(self):
        '''
        Return a dict with hostname, OS, kernel, release.
        '''
        return dict(platform.uname()._asdict())


    def get_cpu_times(self):
        '''
        Returns dict of dicts for each CPU with seconds that it has spent in different modes.
        '''
        # Zip together list of CPUs and their times .
        list_cpu_times = [item._asdict() for item in psutil.cpu_times(percpu=True)]
        return dict(zip(self.list_cpus, list_cpu_times))

    def get_cpu_percent(self):
        '''
        Returns dict of CPU utilizations percentage for each CPU.
        '''
        list_cpus = ['cpu' + str(item) for item in range(psutil.cpu_count(logical=True))]
        # Zip together list of CPUs and their utilisations.
        return dict(zip(self.list_cpus, psutil.cpu_percent(interval=0.5, percpu=True)))

    def get_cpu_times_percent(self):
        '''
        Returns dict of dicts for each CPU with times
        '''
        # Zip together list of CPUs and their times percents.
        list_cpu_times_percents = [item._asdict() for item in psutil.cpu_times_percent(interval=0.5, percpu=True)]
        return dict(zip(self.list_cpus, list_cpu_times_percents))

    def get_cpu_stats(self):
        '''
        Returns dict of CPU interruptions and context switches.
        '''
        return psutil.cpu_stats()._asdict()

    def get_cpu_freq(self):
        '''
        Returns dict of dicts for each CPU with current, min and max frequencies expressed in Mhz.
        '''
        # Zip together list of CPUs and their frequencies stats.
        list_cpu_freqs = [item._asdict() for item in psutil.cpu_freq(percpu=True)]
        return dict(zip(self.list_cpus, list_cpu_freqs))

    def get_load_average(self):
        '''
        Returns a dict with average load over the last 1, 5 and 15 minutes.
        '''
        # Zip together load average descriptions and values.
        list1 = ['over_1_min', 'over_5_min', 'over_15_min']
        list2 = list(psutil.getloadavg())
        return dict(zip(list1, list2))

    def to_json(self):
        return json.dumps(self.metrics)

