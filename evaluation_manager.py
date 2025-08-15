import importlib
from typing import Dict, Any, Union, Optional
from evaluators.evaluation_types import EvaluationType


class EvaluationManager:
    def __init__(self, evaluation_type: EvaluationType, evaluator: str, evaluator_model: str):
        self.evaluation_type = evaluation_type
        self.evaluator = evaluator
        self.evaluator_model = evaluator_model
        self.evaluate_function = self._load_evaluator()
    
    def _load_evaluator(self):
        try:
            evaluator_module = importlib.import_module(f'evaluators.{self.evaluation_type.value}')
            return evaluator_module.evaluate
        except ImportError:
            raise ValueError(f"Evaluator '{self.evaluation_type.value}' not found. Available evaluators: problem_solving, simple_question")
    
    def evaluate_response(self, question: str, expected_answer: Optional[str], 
                         actual_answer: str) -> Dict[str, Any]:
        evaluation = self.evaluate_function(
            evaluator=self.evaluator,
            evaluator_model=self.evaluator_model,
            question=question,
            expected_answer=expected_answer,
            answer=actual_answer
        )
        
        # Handle both old format (string) and new format (dict)
        if isinstance(evaluation, dict):
            return {
                'score': evaluation['score'],
                'reasoning': evaluation['reasoning']
            }
        else:
            return {
                'score': evaluation,
                'reasoning': 'No reasoning provided'
            }
    
    def display_evaluation_results(self, evaluation_result: Dict[str, Any]) -> None:
        print("Evaluating Response...")
        print(f"Evaluation Score: {evaluation_result['score']}")
        print(f"Evaluation Reasoning: {evaluation_result['reasoning']}")
        print("-" * 50)