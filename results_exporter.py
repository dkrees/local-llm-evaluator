import csv
from typing import List, Dict, Any


class ResultsExporter:
    def __init__(self, output_filename: str = 'test_results.csv'):
        self.output_filename = output_filename
        self.fieldnames = [
            'question_number', 'test_number', 'question', 'llm_answer', 'expected_answer',
            'model_name', 'evaluator', 'evaluator_model', 'prompt_tokens', 'completion_tokens',
            'total_tokens', 'response_time', 'energy_usage', 'evaluation_score', 'evaluation_reasoning'
        ]
    
    def export_to_csv(self, csv_data: List[Dict[str, Any]]) -> None:
        with open(self.output_filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=self.fieldnames)
            writer.writeheader()
            writer.writerows(csv_data)
        
        print(f"\nResults exported to {self.output_filename}")
    
