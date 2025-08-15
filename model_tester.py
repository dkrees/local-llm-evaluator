from typing import Dict, Any, List, Optional
from test_subject import test_model
from evaluators.evaluation_types import EvaluationType


class ModelTester:
    def __init__(self, evaluation_type: EvaluationType):
        self.evaluation_type = evaluation_type

    def test_single_iteration(self, provider: str, model: str, question: str) -> Dict[str, Any]:
        response = test_model(
            provider=provider,
            model=model,
            evaluation_type=self.evaluation_type,
            question=question
        )
        return response

    def run_multiple_tests(self, provider: str, model: str, question: str,
                          num_tests: int) -> List[Dict[str, Any]]:
        results = []
        for _ in range(num_tests):
            result = self.test_single_iteration(provider, model, question)
            results.append(result)
        return results

    def test_question_batch(self, model_config: Dict[str, str], question: str,
                           expected_answer: Optional[str], question_num: int,
                           num_tests: int) -> Dict[str, Any]:

        print(f"\nQuestion {question_num}: {question}")
        if expected_answer:
            print(f"Expected Answer: {expected_answer}")
        else:
            print("Expected Answer: None (question-only dataset)")

        responses = []
        for j in range(num_tests):
            print(f"\nQuestion {question_num}, Test {j+1}: {question}")

            response = self.test_single_iteration(
                model_config['provider'],
                model_config['model'],
                question
            )

            self._display_response_details(response)
            responses.append(response)

        return {
            'responses': responses,
            'question': question,
            'expected_answer': expected_answer,
            'question_num': question_num
        }

    def _display_response_details(self, response: Dict[str, Any]) -> None:
        print("-" * 50)
        print(f"AI Answer: {response['response']}")
        print("-" * 50)
        print(f"Prompt Tokens: {response['prompt_tokens']}")
        print(f"Completion Tokens: {response['completion_tokens']}")
        print(f"Total Tokens: {response['total_tokens']}")
        print("-" * 50)
        print(f"Response Time: {response['response_time']:.2f} seconds")