from test_subject import test_model
from utility import parse_input_data
from powermetrics import PowerMetricsCollector
import statistics
import csv
import importlib
import yaml
from evaluators.evaluation_types import EvaluationType

def load_config(config_path='config.yml'):
    with open(config_path, 'r') as file:
        config = yaml.safe_load(file)
    # Convert evaluation_type string to enum
    config['evaluation_type'] = EvaluationType[config['evaluation_type']]
    return config

def main():
    # Load configuration
    config = load_config()
    subject_models = config['subject_models']
    evaluator = config['evaluator']
    evaluator_model = config['evaluator_model']
    number_of_tests = config['number_of_tests']
    dataset = config['dataset']
    evaluation_type = config['evaluation_type']

    # Dynamically import the evaluator based on evaluation_type
    try:
        evaluator_module = importlib.import_module(f'evaluators.{evaluation_type.value}')
        evaluate = evaluator_module.evaluate
    except ImportError:
        raise ValueError(f"Evaluator '{evaluation_type.value}' not found. Available evaluators: problem_solving, simple_question")

    qa_pairs = parse_input_data(dataset)

    # Collect all test results for CSV export
    csv_data = []

    # Dictionary to store metrics per model
    model_metrics = {}

    for m, model in enumerate(subject_models):
        print(f"\n{'='*60}")
        print(f"Testing Provider and Model: {model['provider']} - {model['model']}")
        print(f"{'='*60}")

        # Lists to calculate model-specific averages
        model_evaluation_scores = []
        model_response_times = []
        model_completion_tokens = []
        model_total_tokens = []
        model_energy_usage = []

        for i, qa in enumerate(qa_pairs, 1):
            question_evaluation_scores = []
            question_response_times = []
            question_completion_tokens = []
            question_total_tokens = []
            question_energy_usage = []

            expected_answer = None

            for j in range(number_of_tests):

                print(f"\nQuestion {i}, Test {j+1}: {qa['question']}")
                if qa['answer']:
                    print(f"Expected Answer: {qa['answer']}")
                    expected_answer = qa['answer']
                else:
                    print("Expected Answer: None (question-only dataset)")

                # Start energy monitoring
                power_collector = PowerMetricsCollector()
                power_collector.start_collection()
                
                # TEST THE MODEL
                response = test_model(
                    provider = model['provider'],
                    model = model['model'],
                    evaluation_type = evaluation_type,
                    question = qa['question']
                )
                
                # Stop energy monitoring and get average
                energy_usage = power_collector.stop_collection()

                print(f"AI Answer: {response['response']}")
                print("-" * 50)
                print(f"Prompt Tokens: {response['prompt_tokens']}")
                print(f"Completion Tokens: {response['completion_tokens']}")
                print(f"Total Tokens: {response['total_tokens']}")
                print("-" * 50)
                print(f"Response Time: {response['response_time']:.2f} seconds")
                if energy_usage is not None:
                    print(f"Energy Usage: {energy_usage:.2f} mW")
                else:
                    print("Energy Usage: N/A (powermetrics failed)")
                print("-" * 50)
                print("Evaluating Response...")

                # Evaluation
                evaluation = evaluate(
                    evaluator=evaluator,
                    evaluator_model=evaluator_model,
                    question=qa['question'],
                    expected_answer=expected_answer,
                    answer=response["response"]
                )

                # Handle both old format (string) and new format (dict)
                if isinstance(evaluation, dict):
                    evaluation_score = evaluation['score']
                    evaluation_reasoning = evaluation['reasoning']
                else:
                    evaluation_score = evaluation
                    evaluation_reasoning = 'No reasoning provided'

                print(f"Evaluation Score: {evaluation_score}")
                print(f"Evaluation Reasoning: {evaluation_reasoning}")
                print("-" * 50)

                # Collect metrics for question-specific averages
                question_evaluation_scores.append(float(evaluation_score))
                question_response_times.append(response['response_time'])
                question_completion_tokens.append(response['completion_tokens'])
                question_total_tokens.append(response['total_tokens'])
                if energy_usage is not None:
                    question_energy_usage.append(energy_usage)

                # Collect metrics for model-specific averages
                model_evaluation_scores.append(float(evaluation_score))
                model_response_times.append(response['response_time'])
                model_completion_tokens.append(response['completion_tokens'])
                model_total_tokens.append(response['total_tokens'])
                if energy_usage is not None:
                    model_energy_usage.append(energy_usage)

                # Collect data for CSV
                csv_data.append({
                    'question_number': i,
                    'test_number': j+1,
                    'question': qa['question'],
                    'llm_answer': response['response'],
                    'expected_answer': expected_answer if expected_answer else '',
                    'model_name': model['model'],
                    'evaluator': evaluator,
                    'evaluator_model': evaluator_model,
                    'prompt_tokens': response['prompt_tokens'],
                    'completion_tokens': response['completion_tokens'],
                    'total_tokens': response['total_tokens'],
                    'response_time': f"{response['response_time']:.2f}",
                    'energy_usage': f"{energy_usage:.2f}" if energy_usage is not None else 'N/A',
                    'evaluation_score': f"{float(evaluation_score):.2f}",
                    'evaluation_reasoning': evaluation_reasoning
                })

            # Calculate per-question averages
            avg_score = statistics.mean(question_evaluation_scores)
            avg_question_response_time = statistics.mean(question_response_times)
            avg_question_completion_tokens = statistics.mean(question_completion_tokens)
            avg_question_total_tokens = statistics.mean(question_total_tokens)
            avg_question_energy_usage = statistics.mean(question_energy_usage) if question_energy_usage else None

            print("=" * 50)
            print(f"📈 Question {i} Averages:")
            print(f"  Score: {avg_score:.2f}")
            print(f"  Response Time: {avg_question_response_time:.2f} seconds")
            print(f"  Completion Tokens: {avg_question_completion_tokens:.2f}")
            print(f"  Total Tokens: {avg_question_total_tokens:.2f}")
            if avg_question_energy_usage is not None:
                print(f"  Energy Usage: {avg_question_energy_usage:.2f} mW")
            else:
                print(f"  Energy Usage: N/A")

            # Add per-question averages row to CSV data
            csv_data.append({
                'question_number': i,
                'test_number': 'Average',
                'question': '',
                'llm_answer': '',
                'expected_answer': '',
                'model_name': '',
                'evaluator': '',
                'evaluator_model': '',
                'prompt_tokens': '',
                'completion_tokens': f"{avg_question_completion_tokens:.2f}",
                'total_tokens': f"{avg_question_total_tokens:.2f}",
                'response_time': f"{avg_question_response_time:.2f}",
                'energy_usage': f"{avg_question_energy_usage:.2f}" if avg_question_energy_usage is not None else 'N/A',
                'evaluation_score': f"{avg_score:.2f}",
                'evaluation_reasoning': ''
            })

        # Calculate model-specific averages
        model_avg_score = statistics.mean(model_evaluation_scores)
        model_avg_response_time = statistics.mean(model_response_times)
        model_avg_completion_tokens = statistics.mean(model_completion_tokens)
        model_avg_total_tokens = statistics.mean(model_total_tokens)
        model_avg_energy_usage = statistics.mean(model_energy_usage) if model_energy_usage else None

        # Store model metrics for comparison
        model_metrics[model['model']] = {
            'avg_score': model_avg_score,
            'avg_response_time': model_avg_response_time,
            'avg_completion_tokens': model_avg_completion_tokens,
            'avg_total_tokens': model_avg_total_tokens,
            'avg_energy_usage': model_avg_energy_usage
        }

        # Print model-specific averages to console
        print("=" * 60)
        print(f"MODEL AVERAGES FOR {model['model']}:")
        print(f"Average Score: {model_avg_score:.2f}")
        print(f"Average Response Time: {model_avg_response_time:.2f} seconds")
        print(f"Average Completion Tokens: {model_avg_completion_tokens:.2f}")
        print(f"Average Total Tokens: {model_avg_total_tokens:.2f}")
        if model_avg_energy_usage is not None:
            print(f"Average Energy Usage: {model_avg_energy_usage:.2f} mW")
        else:
            print(f"Average Energy Usage: N/A")
        print("=" * 60)

        # Add model averages row to CSV data
        csv_data.append({
            'question_number': f"Model_{model['model']}_Average",
            'test_number': 'Average',
            'question': '',
            'llm_answer': '',
            'expected_answer': '',
            'model_name': model['model'],
            'evaluator': evaluator,
            'evaluator_model': evaluator_model,
            'prompt_tokens': '',
            'completion_tokens': f"{model_avg_completion_tokens:.2f}",
            'total_tokens': f"{model_avg_total_tokens:.2f}",
            'response_time': f"{model_avg_response_time:.2f}",
            'energy_usage': f"{model_avg_energy_usage:.2f}" if model_avg_energy_usage is not None else 'N/A',
            'evaluation_score': f"{model_avg_score:.2f}",
            'evaluation_reasoning': ''
        })

    # Find the winning model
    winning_model = max(model_metrics.items(), key=lambda x: x[1]['avg_score'])
    winning_model_name = winning_model[0]
    winning_score = winning_model[1]['avg_score']

    # Print model comparison and declare winner
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
            print(f"  Average Energy Usage: {metrics['avg_energy_usage']:.2f} mW")
        else:
            print(f"  Average Energy Usage: N/A")
        print()

    print("🏆 WINNING MODEL 🏆")
    print(f"Model: {winning_model_name}")
    print(f"Highest Average Score: {winning_score:.2f}")
    print("=" * 80)

    # Write to CSV file
    with open('test_results.csv', 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['question_number', 'test_number', 'question', 'llm_answer', 'expected_answer', 'model_name', 'evaluator', 'evaluator_model', 'prompt_tokens', 'completion_tokens', 'total_tokens', 'response_time', 'energy_usage', 'evaluation_score', 'evaluation_reasoning']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(csv_data)

    print(f"\nResults exported to test_results.csv")


if __name__ == "__main__":
    main()