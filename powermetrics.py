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
        """
        Collect power reading
        -i: interval in ms
        -n: number of samples
        Outputs the combined CPU, GPU and ANE in mW
        """
        try:
            cmd = "sudo powermetrics -i 100 -n 10 --samplers cpu_power | grep 'Combined Power'"
            output = subprocess.check_output(cmd, shell=True, universal_newlines=True, stderr=subprocess.STDOUT)

            pattern = r'Combined Power \(CPU \+ GPU \+ ANE\):\s+(\d+)\s+mW'
            match = re.search(pattern, output)
            if match:
                mw_value = int(match.group(1))
                watts_value = mw_value / 1000.0  # Convert mW to W
                return watts_value
            else:
                print(f"PowerMetrics: Could not parse power reading from output: '{output}'")
                print(f"PowerMetrics: Pattern used: {pattern}")
                return None
        except subprocess.CalledProcessError as e:
            print(f"PowerMetrics: Command failed with error: {e}")
            print(f"PowerMetrics: Output: {e.output}")
            return None
        except Exception as e:
            print(f"PowerMetrics: Unexpected error: {e}")
            return None

    def _collection_loop(self):
        """Continuously collect 10 power readings every 1 seconds"""
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

# def get_cpu_power_usage():
#     """Legacy function for backward compatibility"""
#     try:
#         cmd = ["sudo", "powermetrics", "-n", "1", "--samplers", "cpu_power", "gpu_power"]
#         output = subprocess.check_output(cmd, universal_newlines=True)

#         pattern = r'CPU Power:\s+(\d+)\s+mW'
#         match = re.search(pattern, output)
#         if match:
#             cpu_power_usage = int(match.group(1))
#             return cpu_power_usage
#         else:
#             print("Failed to extract CPU power usage from powermetrics output.")
#             return None

#     except subprocess.CalledProcessError as e:
#         print(f"Error running powermetrics with sudo: {e}")
#         return None

# if __name__ == "__main__":
#     cpu_power = get_cpu_power_usage()
#     if cpu_power is not None:
#         print(f"Current CPU Power Usage: {cpu_power} mW")
