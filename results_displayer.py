from typing import Dict, Any, Optional


class ResultsDisplayer:
    def __init__(self):
        pass
    
    def display_model_header(self, provider: str, model: str) -> None:
        print(f"\n{'='*60}")
        print(f"Testing Provider and Model: {provider} - {model}")
        print(f"{'='*60}")
    
    def display_question_header(self, question_num: int, test_num: int, question: str) -> None:
        print(f"\nQuestion {question_num}, Test {test_num}: {question}")
    
    def display_expected_answer(self, expected_answer: Optional[str]) -> None:
        if expected_answer:
            print(f"Expected Answer: {expected_answer}")
        else:
            print("Expected Answer: None (question-only dataset)")
    
    def display_response_details(self, response: Dict[str, Any]) -> None:
        print(f"AI Answer: {response['response']}")
        print("-" * 50)
        print(f"Prompt Tokens: {response['prompt_tokens']}")
        print(f"Completion Tokens: {response['completion_tokens']}")
        print(f"Total Tokens: {response['total_tokens']}")
        print("-" * 50)
        print(f"Response Time: {response['response_time']:.2f} seconds")
    
    def display_power_metrics(self, energy_usage: Optional[float], response_time: float) -> None:
        if energy_usage is not None:
            energy_consumption_wh = energy_usage * (response_time / 3600)
            print(f"Power Usage: {energy_usage:.3f} W")
            print(f"Energy Consumption: {energy_consumption_wh:.6f} Wh")
        else:
            print("Power Usage: N/A")
            print("Energy Consumption: N/A")
        print("-" * 50)
    
    def display_question_averages(self, question_num: int, metrics: Dict[str, Optional[float]]) -> None:
        print("=" * 50)
        print(f"📈 Question {question_num} Averages:")
        print(f"  Score: {metrics['avg_score']:.2f}")
        print(f"  Response Time: {metrics['avg_response_time']:.2f} seconds")
        print(f"  Completion Tokens: {metrics['avg_completion_tokens']:.2f}")
        print(f"  Total Tokens: {metrics['avg_total_tokens']:.2f}")
        if metrics['avg_energy_usage'] is not None:
            print(f"  Energy Consumption: {metrics['avg_energy_usage']:.6f} Wh")
        else:
            print(f"  Energy Consumption: N/A")
    
    def display_model_averages(self, model_name: str, metrics: Dict[str, Optional[float]]) -> None:
        print("=" * 60)
        print(f"MODEL AVERAGES FOR {model_name}:")
        print(f"Average Score: {metrics['avg_score']:.2f}")
        print(f"Average Response Time: {metrics['avg_response_time']:.2f} seconds")
        print(f"Average Completion Tokens: {metrics['avg_completion_tokens']:.2f}")
        print(f"Average Total Tokens: {metrics['avg_total_tokens']:.2f}")
        if metrics['avg_energy_usage'] is not None:
            print(f"Average Energy Consumption: {metrics['avg_energy_usage']:.6f} Wh")
        else:
            print(f"Average Energy Consumption: N/A")
        print("=" * 60)
    
    def display_model_comparison(self, model_metrics: Dict[str, Dict[str, Optional[float]]]) -> None:
        print("\n" + "=" * 80)
        print("MODEL COMPARISON SUMMARY:")
        print("=" * 80)
        for model_name, metrics in model_metrics.items():
            print(f"{model_name}:")
            print(f"  Average Score: {metrics['avg_score']:.2f}")
            print(f"  Average Response Time: {metrics['avg_response_time']:.2f}s")
            print(f"  Average Completion Tokens: {metrics['avg_completion_tokens']:.2f}")
            print(f"  Average Total Tokens: {metrics['avg_total_tokens']:.2f}")
            if metrics['avg_energy_usage'] is not None:
                print(f"  Average Energy Consumption: {metrics['avg_energy_usage']:.6f} Wh")
            else:
                print(f"  Average Energy Consumption: N/A")
            print()
    
    def display_winning_model(self, winning_model_name: str, winning_score: float) -> None:
        print("🏆 WINNING MODEL 🏆")
        print(f"Model: {winning_model_name}")
        print(f"Highest Average Score: {winning_score:.2f}")
        print("=" * 80)