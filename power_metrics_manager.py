from typing import Optional
from powermetrics import PowerMetricsCollector


class PowerMetricsManager:
    def __init__(self, enabled: bool = False):
        self.enabled = enabled
        self.power_collector = None
        
    def start_monitoring(self) -> None:
        if self.enabled:
            self.power_collector = PowerMetricsCollector()
            self.power_collector.start_collection()
    
    def stop_monitoring(self) -> Optional[float]:
        if self.enabled and self.power_collector:
            energy_usage = self.power_collector.stop_collection()
            return energy_usage
        return None
    
    def calculate_energy_consumption(self, energy_usage: Optional[float], 
                                   response_time: float) -> Optional[float]:
        if energy_usage is not None and response_time > 0:
            # Calculate energy consumption in Wh: Power (W) × Time (hours)
            return energy_usage * (response_time / 3600)
        return None
    
    def display_power_metrics(self, energy_usage: Optional[float], 
                            response_time: float) -> None:
        if energy_usage is not None:
            energy_consumption_wh = self.calculate_energy_consumption(energy_usage, response_time)
            print(f"Power Usage: {energy_usage:.3f} W")
            print(f"Energy Consumption: {energy_consumption_wh:.6f} Wh")
        else:
            print("Power Usage: N/A")
            print("Energy Consumption: N/A")