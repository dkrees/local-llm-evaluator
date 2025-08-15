import statistics
from typing import Dict, List, Any, Optional


class MetricsCollector:
    def __init__(self):
        self.reset()
    
    def reset(self):
        self.evaluation_scores = []
        self.response_times = []
        self.completion_tokens = []
        self.total_tokens = []
        self.energy_usage = []
    
    def add_metric(self, evaluation_score: float, response_time: float, 
                   completion_tokens: int, total_tokens: int, 
                   energy_consumption_wh: Optional[float] = None):
        self.evaluation_scores.append(evaluation_score)
        self.response_times.append(response_time)
        self.completion_tokens.append(completion_tokens)
        self.total_tokens.append(total_tokens)
        if energy_consumption_wh is not None:
            self.energy_usage.append(energy_consumption_wh)
    
    def get_averages(self) -> Dict[str, Optional[float]]:
        return {
            'avg_score': statistics.mean(self.evaluation_scores) if self.evaluation_scores else 0,
            'avg_response_time': statistics.mean(self.response_times) if self.response_times else 0,
            'avg_completion_tokens': statistics.mean(self.completion_tokens) if self.completion_tokens else 0,
            'avg_total_tokens': statistics.mean(self.total_tokens) if self.total_tokens else 0,
            'avg_energy_usage': statistics.mean(self.energy_usage) if self.energy_usage else None
        }
    
    def get_raw_metrics(self) -> Dict[str, List]:
        return {
            'evaluation_scores': self.evaluation_scores.copy(),
            'response_times': self.response_times.copy(),
            'completion_tokens': self.completion_tokens.copy(),
            'total_tokens': self.total_tokens.copy(),
            'energy_usage': self.energy_usage.copy()
        }


class QuestionMetricsCollector(MetricsCollector):
    def __init__(self, question_num: int, question: str):
        super().__init__()
        self.question_num = question_num
        self.question = question
    
    def create_csv_row(self, test_num: int, question: str, llm_answer: str, 
                       expected_answer: str, model_name: str, evaluator: str,
                       evaluator_model: str, prompt_tokens: int, completion_tokens: int,
                       total_tokens: int, response_time: float, energy_usage: Optional[float],
                       evaluation_score: float, evaluation_reasoning: str) -> Dict[str, str]:
        return {
            'question_number': self.question_num,
            'test_number': test_num,
            'question': question,
            'llm_answer': llm_answer,
            'expected_answer': expected_answer if expected_answer else '',
            'model_name': model_name,
            'evaluator': evaluator,
            'evaluator_model': evaluator_model,
            'prompt_tokens': prompt_tokens,
            'completion_tokens': completion_tokens,
            'total_tokens': total_tokens,
            'response_time': f"{response_time:.2f}",
            'energy_usage': f"{energy_usage:.6f}" if energy_usage is not None else 'N/A',
            'evaluation_score': f"{evaluation_score:.2f}",
            'evaluation_reasoning': evaluation_reasoning
        }
    
    def create_average_csv_row(self) -> Dict[str, str]:
        averages = self.get_averages()
        return {
            'question_number': self.question_num,
            'test_number': 'Average',
            'question': '',
            'llm_answer': '',
            'expected_answer': '',
            'model_name': '',
            'evaluator': '',
            'evaluator_model': '',
            'prompt_tokens': '',
            'completion_tokens': f"{averages['avg_completion_tokens']:.2f}",
            'total_tokens': f"{averages['avg_total_tokens']:.2f}",
            'response_time': f"{averages['avg_response_time']:.2f}",
            'energy_usage': f"{averages['avg_energy_usage']:.6f}" if averages['avg_energy_usage'] is not None else 'N/A',
            'evaluation_score': f"{averages['avg_score']:.2f}",
            'evaluation_reasoning': ''
        }


class ModelMetricsCollector(MetricsCollector):
    def __init__(self, model_name: str):
        super().__init__()
        self.model_name = model_name
    
    def create_model_average_csv_row(self, evaluator: str, evaluator_model: str) -> Dict[str, str]:
        averages = self.get_averages()
        return {
            'question_number': f"Model_{self.model_name}_Average",
            'test_number': 'Average',
            'question': '',
            'llm_answer': '',
            'expected_answer': '',
            'model_name': self.model_name,
            'evaluator': evaluator,
            'evaluator_model': evaluator_model,
            'prompt_tokens': '',
            'completion_tokens': f"{averages['avg_completion_tokens']:.2f}",
            'total_tokens': f"{averages['avg_total_tokens']:.2f}",
            'response_time': f"{averages['avg_response_time']:.2f}",
            'energy_usage': f"{averages['avg_energy_usage']:.6f}" if averages['avg_energy_usage'] is not None else 'N/A',
            'evaluation_score': f"{averages['avg_score']:.2f}",
            'evaluation_reasoning': ''
        }