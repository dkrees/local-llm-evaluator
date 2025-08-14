import subprocess
import re
import time
import threading
import statistics

class PowerMetricsCollector:
    def __init__(self):
        self.power_readings = []
        self.is_collecting = False
        self.collection_thread = None

    def _collect_power_reading(self):
        """Collect a single power reading"""
        try:
            cmd = ["sudo", "powermetrics", "-n", "1", "--samplers", "cpu_power"]
            output = subprocess.check_output(cmd, universal_newlines=True)
            
            pattern = r'CPU Power:\s+(\d+)\s+mW'
            match = re.search(pattern, output)
            if match:
                return int(match.group(1))
            else:
                return None
        except subprocess.CalledProcessError:
            return None

    def _collection_loop(self):
        """Continuously collect power readings every 0.5 seconds"""
        while self.is_collecting:
            reading = self._collect_power_reading()
            if reading is not None:
                self.power_readings.append(reading)
            time.sleep(0.5)

    def start_collection(self):
        """Start collecting power metrics"""
        self.power_readings = []
        self.is_collecting = True
        self.collection_thread = threading.Thread(target=self._collection_loop)
        self.collection_thread.start()

    def stop_collection(self):
        """Stop collecting power metrics and return average"""
        self.is_collecting = False
        if self.collection_thread:
            self.collection_thread.join()
        
        if self.power_readings:
            return statistics.mean(self.power_readings)
        else:
            return None

def get_cpu_power_usage():
    """Legacy function for backward compatibility"""
    try:
        cmd = ["sudo", "powermetrics", "-n", "1", "--samplers", "cpu_power"]
        output = subprocess.check_output(cmd, universal_newlines=True)

        pattern = r'CPU Power:\s+(\d+)\s+mW'
        match = re.search(pattern, output)
        if match:
            cpu_power_usage = int(match.group(1))
            return cpu_power_usage
        else:
            print("Failed to extract CPU power usage from powermetrics output.")
            return None

    except subprocess.CalledProcessError as e:
        print(f"Error running powermetrics with sudo: {e}")
        return None

if __name__ == "__main__":
    cpu_power = get_cpu_power_usage()
    if cpu_power is not None:
        print(f"Current CPU Power Usage: {cpu_power} mW")
