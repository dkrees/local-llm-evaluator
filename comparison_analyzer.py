from typing import Dict, Tuple, Optional


class ComparisonAnalyzer:
    def __init__(self):
        pass

    def find_winning_model(self, model_metrics: Dict[str, Dict[str, Optional[float]]]) -> Tuple[str, float]:
        if not model_metrics:
            raise ValueError("No model metrics provided for comparison")

        winning_model = max(model_metrics.items(), key=lambda x: x[1]['avg_score'])
        winning_model_name = winning_model[0]
        winning_score = winning_model[1]['avg_score']

        return winning_model_name, winning_score

    def rank_models_by_score(self, model_metrics: Dict[str, Dict[str, Optional[float]]]) -> list:
        return sorted(model_metrics.items(), key=lambda x: x[1]['avg_score'], reverse=True)

    def rank_models_by_efficiency(self, model_metrics: Dict[str, Dict[str, Optional[float]]]) -> list:
        # Rank by score/response_time ratio (higher is better)
        def efficiency_score(metrics):
            if metrics['avg_response_time'] > 0:
                return metrics['avg_score'] / metrics['avg_response_time']
            return 0

        return sorted(model_metrics.items(), key=lambda x: efficiency_score(x[1]), reverse=True)

    def rank_models_by_energy_efficiency(self, model_metrics: Dict[str, Dict[str, Optional[float]]]) -> list:
        # Rank by score/energy_usage ratio (higher is better), excluding models without energy data
        valid_models = [(name, metrics) for name, metrics in model_metrics.items()
                       if metrics['avg_energy_usage'] is not None and metrics['avg_energy_usage'] > 0]

        def energy_efficiency_score(metrics):
            return metrics['avg_score'] / metrics['avg_energy_usage']

        return sorted(valid_models, key=lambda x: energy_efficiency_score(x[1]), reverse=True)

    def get_model_statistics(self, model_metrics: Dict[str, Dict[str, Optional[float]]]) -> Dict[str, any]:
        if not model_metrics:
            return {}

        scores = [metrics['avg_score'] for metrics in model_metrics.values()]
        response_times = [metrics['avg_response_time'] for metrics in model_metrics.values()]

        return {
            'total_models': len(model_metrics),
            'highest_score': max(scores),
            'lowest_score': min(scores),
            'average_score': sum(scores) / len(scores),
            'fastest_response_time': min(response_times),
            'slowest_response_time': max(response_times),
            'average_response_time': sum(response_times) / len(response_times)
        }