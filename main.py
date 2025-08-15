from config_manager import ConfigManager
from model_tester import ModelTester
from evaluation_manager import EvaluationManager
from power_metrics_manager import PowerMetricsManager
from metrics_collector import QuestionMetricsCollector, ModelMetricsCollector
from results_displayer import ResultsDisplayer
from results_exporter import ResultsExporter
from comparison_analyzer import ComparisonAnalyzer
from utility import parse_input_data
from typing import Dict, List, Any


class LocalLLMTestSuite:
    def __init__(self, config_path: str = 'config.yml'):
        self.config = ConfigManager(config_path)
        self.model_tester = ModelTester(self.config.evaluation_type)
        self.evaluation_manager = EvaluationManager(
            self.config.evaluation_type,
            self.config.evaluator,
            self.config.evaluator_model
        )
        self.power_manager = PowerMetricsManager(self.config.powermetrics)
        self.displayer = ResultsDisplayer()
        self.exporter = ResultsExporter()
        self.analyzer = ComparisonAnalyzer()

    def run_complete_test_suite(self) -> None:
        qa_pairs = parse_input_data(self.config.dataset)
        csv_data = []
        model_metrics = {}

        for model in self.config.subject_models:
            model_results = self._test_model(model, qa_pairs)
            model_metrics[model['model']] = model_results['metrics']
            csv_data.extend(model_results['csv_data'])

        self._display_final_results(model_metrics)
        self.exporter.export_to_csv(csv_data)

    def _test_model(self, model: Dict[str, str], qa_pairs: List[Dict[str, str]]) -> Dict[str, Any]:
        self.displayer.display_model_header(model['provider'], model['model'])

        model_collector = ModelMetricsCollector(model['model'])
        csv_data = []

        for i, qa in enumerate(qa_pairs, 1):
            question_results = self._test_question(model, qa, i)

            # Add individual test results to model collector
            for result in question_results['individual_results']:
                model_collector.add_metric(
                    result['evaluation_score'],
                    result['response_time'],
                    result['completion_tokens'],
                    result['total_tokens'],
                    result['energy_consumption_wh']
                )

            csv_data.extend(question_results['csv_data'])
            self.displayer.display_question_averages(i, question_results['averages'])

        # Display and add model averages
        model_averages = model_collector.get_averages()
        self.displayer.display_model_averages(model['model'], model_averages)
        csv_data.append(model_collector.create_model_average_csv_row(
            self.config.evaluator, self.config.evaluator_model
        ))

        return {
            'metrics': model_averages,
            'csv_data': csv_data
        }

    def _test_question(self, model: Dict[str, str], qa: Dict[str, str], question_num: int) -> Dict[str, Any]:
        question_collector = QuestionMetricsCollector(question_num, qa['question'])
        csv_data = []
        individual_results = []

        expected_answer = qa['answer'] if qa['answer'] else None

        for j in range(self.config.number_of_tests):
            result = self._run_single_test(model, qa, question_num, j + 1, expected_answer)

            question_collector.add_metric(
                result['evaluation_score'],
                result['response_time'],
                result['completion_tokens'],
                result['total_tokens'],
                result['energy_consumption_wh']
            )

            csv_data.append(question_collector.create_csv_row(
                j + 1, qa['question'], result['llm_answer'],
                expected_answer or '', model['model'], self.config.evaluator,
                self.config.evaluator_model, result['prompt_tokens'],
                result['completion_tokens'], result['total_tokens'],
                result['response_time'], result['energy_consumption_wh'],
                result['evaluation_score'], result['evaluation_reasoning']
            ))

            individual_results.append(result)

        # Add question averages to CSV
        csv_data.append(question_collector.create_average_csv_row())

        return {
            'averages': question_collector.get_averages(),
            'csv_data': csv_data,
            'individual_results': individual_results
        }

    def _run_single_test(self, model: Dict[str, str], qa: Dict[str, str],
                        question_num: int, test_num: int, expected_answer: str) -> Dict[str, Any]:

        self.displayer.display_question_header(question_num, test_num, qa['question'])
        self.displayer.display_expected_answer(expected_answer)

        # Start power monitoring
        self.power_manager.start_monitoring()

        # Test the model
        response = self.model_tester.test_single_iteration(
            model['provider'], model['model'], qa['question']
        )

        # Stop power monitoring
        energy_usage = self.power_manager.stop_monitoring()
        energy_consumption_wh = self.power_manager.calculate_energy_consumption(
            energy_usage, response['response_time']
        )

        # Display response details
        self.displayer.display_response_details(response)
        self.power_manager.display_power_metrics(energy_usage, response['response_time'])

        # Evaluate response
        evaluation_result = self.evaluation_manager.evaluate_response(
            qa['question'], expected_answer, response['response']
        )
        self.evaluation_manager.display_evaluation_results(evaluation_result)

        return {
            'llm_answer': response['response'],
            'prompt_tokens': response['prompt_tokens'],
            'completion_tokens': response['completion_tokens'],
            'total_tokens': response['total_tokens'],
            'response_time': response['response_time'],
            'energy_consumption_wh': energy_consumption_wh,
            'evaluation_score': float(evaluation_result['score']),
            'evaluation_reasoning': evaluation_result['reasoning']
        }

    def _display_final_results(self, model_metrics: Dict[str, Dict[str, float]]) -> None:
        self.displayer.display_model_comparison(model_metrics)

        winning_model_name, winning_score = self.analyzer.find_winning_model(model_metrics)
        self.displayer.display_winning_model(winning_model_name, winning_score)


def main():
    test_suite = LocalLLMTestSuite()
    test_suite.run_complete_test_suite()


if __name__ == "__main__":
    main()