import subprocess
import re

def get_cpu_power_usage():
    try:
        # Run the powermetrics command with sudo and capture its output
        cmd = ["sudo", "powermetrics", "-n", "1", "--samplers", "cpu_power"]
        output = subprocess.check_output(cmd, universal_newlines=True)

        # Use regular expressions to extract the CPU power usage
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
