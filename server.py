#!/bin/python3
import psutil
import os
import sys
import time
import json
from pid import PidFile

SHORT=0.5

class Server:
    def __init__(self):  
        self.data={}    
    
    def worker_cpu_load(self):
        self.data["cpu_load"]=psutil.cpu_percent(interval=SHORT)
        
    def worker_cpu_freq(self):
        self.data["cpu_freq"]=psutil.cpu_freq().current
        
    def worker_cpu_temp(self):
        self.data["cpu_temp"]=psutil.sensors_temperatures()["acpitz"][0].current

    def worker_used_memory(self):
        self.data["used_memory"]=psutil.virtual_memory().used
    
    def worker_used_swap(self):
        self.data["used_swap"]=psutil.swap_memory().used
        
    def worker_disks_io(self):
        data=psutil.disk_io_counters(perdisk=False)
        try:
            last_time=self.data["disks_time"]
            last_write=self.data["disks_write"]
            last_read=self.data["disks_read"]
        except:
            last_time=0
            last_write=0
            last_read=0
        cur_time=time.time()
        self.data["disks_time"]=cur_time  
        self.data["disks_write"]=data.write_bytes
        self.data["disks_read"]=data.read_bytes
        self.data["disks_write_per_second"]=int((data.write_bytes-last_write)/(cur_time-last_time))
        self.data["disks_read_per_second"]=int((data.read_bytes-last_read)/(cur_time-last_time))
    
    def worker_network_io(self):
        data=psutil.net_io_counters(pernic=True)
        try:
            last_time=self.data["network_time"]
            last_recv=self.data["network_recv"]
            last_sent=self.data["network_sent"]
        except:
            last_time=0
            last_recv=0
            last_sent=0
        cur_time=time.time()
        recv=0
        sent=0
        for i,d in data.items():
            recv+=d.bytes_recv
            sent+=d.bytes_sent
        self.data["network_time"]=cur_time
        self.data["network_recv"]=recv
        self.data["network_sent"]=sent
        self.data["network_recv_per_second"]=int((recv-last_recv)/(cur_time-last_time))
        self.data["network_sent_per_second"]=int((sent-last_sent)/(cur_time-last_time))
    
    def server(self):
        while True:
            pass    
        
    def work(self):
        while True:
            self.worker_cpu_load()
            self.worker_cpu_freq()
            self.worker_cpu_temp()
            self.worker_used_memory()
            self.worker_used_swap()
            self.worker_disks_io()
            self.worker_network_io()

            with open("/tmp/system-stats-server-data.json",'w') as f:
                f.write(json.dumps(self.data))


with PidFile(piddir="/tmp"):
    Server().work()
