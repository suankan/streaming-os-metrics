'''
This is a module with classes implementing gathering OS metrics.
'''

from datetime import datetime
import time
import json
import platform
import psutil


class Metrics():
    '''
    This class gets OS metrics using psutil lib.
    More info: https://psutil.readthedocs.io/en/latest/#psutil-documentation
    '''

    def __init__(self):
        # Create a list of CPUs like ['cpu1', 'cpu2', ... , 'cpuN'] for further zipping
        self.cpus = ['cpu' + str(item)
                     for item in range(psutil.cpu_count(logical=True))]
        self.snapshot_started = time.time()
        self.host_info = self.get_host_info()
        self.cpu_times = self.get_cpu_times()
        self.cpu_percent = self.get_cpu_percent()
        self.cpu_times_percent = self.get_cpu_times_percent()
        self.cpu_stats = self.get_cpu_stats()
        self.cpu_freq = self.get_cpu_freq()
        self.load_average = self.get_load_average()
        self.virtual_memory = self.get_virtual_memory()
        self.swap_memory = self.get_swap_memory()
        self.disk_usage = self.get_disk_usage()
        self.disk_io_counters = self.get_disk_io_counters()
        self.net_io_counters = self.get_net_io_counters()
        self.snapshot_finished = time.time()

    def get_host_info(self):
        '''
        Return a dict with hostname, OS, kernel, release.
        '''
        hostinfo = dict(platform.uname()._asdict())
        # Add boot time
        hostinfo['boot_time'] = datetime.utcfromtimestamp(
            psutil.boot_time()).strftime('%Y-%m-%d %H:%M:%S')
        return hostinfo

    def get_cpu_times(self):
        '''
        Returns dict of dicts for each CPU with seconds that it has spent in different modes.
        '''
        # Zip together list of CPUs and their times .
        list_cpu_times = [item._asdict()
                          for item in psutil.cpu_times(percpu=True)]
        return dict(zip(self.cpus, list_cpu_times))

    def get_cpu_percent(self):
        '''
        Returns dict of CPU utilizations percentage for each CPU.
        '''
        # Zip together list of CPUs and their utilisations.
        return dict(zip(self.cpus, psutil.cpu_percent(interval=0.1, percpu=True)))

    def get_cpu_times_percent(self):
        '''
        Returns dict of dicts for each CPU with times
        '''
        # Zip together list of CPUs and their times percents.
        list_cpu_times_percents = [
            item._asdict() for item in psutil.cpu_times_percent(interval=0.1, percpu=True)]
        return dict(zip(self.cpus, list_cpu_times_percents))

    def get_cpu_stats(self):
        '''
        Returns dict of CPU interruptions and context switches.
        '''
        return psutil.cpu_stats()._asdict()

    def get_cpu_freq(self):
        '''
        Returns dict of dicts for each CPU with
        current, min and max frequencies expressed in Mhz.
        '''
        # Zip together list of CPUs and their frequencies stats.
        list_cpu_freqs = [item._asdict()
                          for item in psutil.cpu_freq(percpu=True)]
        return dict(zip(self.cpus, list_cpu_freqs))

    def get_load_average(self):
        '''
        Returns a dict with average load over the last 1, 5 and 15 minutes.
        '''
        # Zip together load average descriptions and values.
        list1 = ['over_1_min', 'over_5_min', 'over_15_min']
        list2 = list(psutil.getloadavg())
        return dict(zip(list1, list2))

    def get_virtual_memory(self):
        '''
        Returns a dict with statistics about system memory usage.
        '''
        return psutil.virtual_memory()._asdict()

    def get_swap_memory(self):
        '''
        Returns dict with system swap memory statistics.
        '''
        return psutil.swap_memory()._asdict()

    def get_disk_usage(self):
        '''
        Returns a dict with disk usage info for each disk.
        '''
        disks_usage = {}
        for disk in psutil.disk_partitions():
            disks_usage[disk.mountpoint] = psutil.disk_usage(
                disk.mountpoint)._asdict()
        return disks_usage

    def get_disk_io_counters(self):
        '''
        Returns a dict with system-wide disk I/O statistics.
        '''
        return psutil.disk_io_counters()._asdict()

    def get_net_io_counters(self):
        '''
        Returns a dict with system-wide network I/O statistics
        '''
        return psutil.net_io_counters()._asdict()

    def to_json(self):
        '''
        Returns self object converted into JSON.
        '''
        return json.dumps(self.__dict__)
