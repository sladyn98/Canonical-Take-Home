import os
import sys
import time


class DiskStatsTester:
    def __init__(self, disk="sda"):
        self.disk = disk
        self.status = 0
    
    def run_tests(self):
        self.check_if_nvdimm()
        self.check_proc_partitions()
        self.check_proc_diskstats()
        self.check_sys_block()
        self.check_sys_block_stat()
        self.record_stats_begin()
        self.generate_disk_activity()
        # Sleep for a few seconds to allow disk activity to be recorded
        time.sleep(5)
        self.record_stats_end()
        self.check_stats_changed()
        if self.status == 0:
            print(f"PASS: Finished testing stats for {self.disk}")
        sys.exit(self.status)
    
    def check_return_code(self, retval, msg, *output):
        if retval != 0:
            print(f"ERROR: retval {retval} : {msg}", file=sys.stderr)
            if self.status == 0:
                self.status = retval
            if output:
                for item in output:
                    print("output: ", item)
        return retval
    
    # Check if the disk is NVDIMM
    def check_if_nvdimm(self, nvdimm="pmem"):
        if nvdimm in self.disk:
            print(f"Disk {self.disk} appears to be an NVDIMM, skipping")
            sys.exit(self.status)
    
    # Check if proc_partitions is present exit if disk isnt found
    def check_proc_partitions(self):
        if self.disk not in open("/proc/partitions").read():
            self.check_return_code(1, f"Disk {self.disk} not found in /proc/partitions")
    
    # Check if proc_diskstats is present exit if disk isnt found
    def check_proc_diskstats(self):
        if self.disk not in open("/proc/diskstats").read():
            self.check_return_code(1, f"Disk {self.disk} not found in /proc/diskstats")

    # Check if disk name shows up in syst/block   
    def check_sys_block(self):
        if not any(self.disk in f for f in os.listdir("/sys/block/")):
            self.check_return_code(1, f"Disk {self.disk} not found in /sys/block/")
    
    def check_sys_block_stat(self):
        if not os.path.exists(f"/sys/block/{self.disk}/stat") or os.stat(f"/sys/block/{self.disk}/stat").st_size == 0:
            self.check_return_code(1, f"stat is either empty or nonexistent in /sys/block/{self.disk}/")
    
    def record_stats_begin(self):
        with open("/proc/diskstats") as f:
            self.proc_stat_begin = next(line for line in f if self.disk in line)
        with open(f"/sys/block/{self.disk}/stat") as f:
            self.sys_stat_begin = f.read()
    
    # Generate disk activity
    def generate_disk_activity(self):
        os.system(f"hdparm -t /dev/{self.disk} > /dev/null 2>&1")
    
    def record_stats_end(self):
        with open("/proc/diskstats") as f:
            self.proc_stat_end = next(line for line in f if self.disk in line)
        with open(f"/sys/block/{self.disk}/stat") as f:
            self.sys_stat_end = f.read()
    
    def check_stats_changed(self):
        if self.proc_stat_begin == self.proc_stat_end:
            self.check_return_code(1, "Stats in /proc/diskstats did not change", self.proc_stat_begin, self.proc_stat_end)
        if self.sys_stat_begin == self.sys_stat_end:
            self.check_return_code(1, f"Stats in /sys/block/{self.disk}/stat did not change", self.sys_stat_begin, self.sys_stat_end)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <disk>", file=sys.stderr)
        sys.exit(1)
    tester = DiskStatsTester(sys.argv[1])
    tester.run_tests()