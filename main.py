from test_subject import test_model
import statistics
import csv
import importlib
from evaluators.evaluation_types import EvaluationType

# CONFIG
subject_model = "lfm2-1.2b"
evaluator = "openai"         # openai | anthropic
evaluator_model = "gpt-4o-mini"            # ie. gpt-4o-mini, claude-sonnet-4-20250514
number_of_tests = 3
dataset = "test_data/summarise_1.txt"
evaluation_type = EvaluationType.SUMMARISE


def parse_input_data(filename):
    """Parse different file formats: Q&A pairs, Q-only, or plain text."""
    qa_pairs = []

    with open(filename, "r") as f:
        content = f.read().strip()

    filename_lower = filename.lower()

    if 'summarise_' in filename_lower :
        qa_pairs.append({"question": content, "answer": None})
    elif 'questions_' in filename_lower:
         # Handle Q&A or Q-only format
        blocks = content.split('\n\n')

        for block in blocks:
            lines = block.strip().split('\n')

            if len(lines) >= 2:
                question_line = lines[0]
                answer_line = lines[1]

                # Extract question and answer text
                if question_line.startswith('Q: ') and answer_line.startswith('A: '):
                    question = question_line[3:]  # Remove 'Q: '
                    answer = answer_line[3:]      # Remove 'A: '
                    qa_pairs.append({"question": question, "answer": answer})
            elif len(lines) == 1:
                question_line = lines[0]

                # Handle question-only format
                if question_line.startswith('Q: '):
                    question = question_line[3:]  # Remove 'Q: '
                    qa_pairs.append({"question": question, "answer": None})

    return qa_pairs

def main():
    # Dynamically import the evaluator based on evaluation_type
    try:
        evaluator_module = importlib.import_module(f'evaluators.{evaluation_type.value}')
        evaluate = evaluator_module.evaluate
    except ImportError:
        raise ValueError(f"Evaluator '{evaluation_type.value}' not found. Available evaluators: problem_solving, simple_question")

    qa_pairs = parse_input_data(dataset)

    # Collect all test results for CSV export
    csv_data = []

    # Lists to calculate overall averages
    all_evaluation_scores = []
    all_response_times = []
    all_completion_tokens = []
    all_total_tokens = []

    for i, qa in enumerate(qa_pairs, 1):
        question_evaluation_scores = []
        question_response_times = []
        question_completion_tokens = []
        question_total_tokens = []

        expected_answer = None

        for j in range(number_of_tests):

            print(f"\nQuestion {i}, Test {j+1}: {qa['question']}")
            if qa['answer']:
                print(f"Expected Answer: {qa['answer']}")
                expected_answer = qa['answer']
            else:
                print("Expected Answer: None (question-only dataset)")

            response = test_model(
                model = subject_model,
                evaluation_type = evaluation_type,
                question = qa['question']
            )

            print(f"AI Answer: {response["response"]}")
            print("-" * 50)
            print(f"Prompt Tokens: {response["prompt_tokens"]}")
            print(f"Completion Tokens: {response["completion_tokens"]}")
            print(f"Total Tokens: {response["total_tokens"]}")
            print("-" * 50)
            print(f"Response Time: {response["response_time"]:.2f} seconds")
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
            print(f"Evaluation Score: {evaluation}")
            print("-" * 50)

            # Collect metrics for question-specific averages
            question_evaluation_scores.append(float(evaluation))
            question_response_times.append(response["response_time"])
            question_completion_tokens.append(response["completion_tokens"])
            question_total_tokens.append(response["total_tokens"])

            # Collect metrics for overall averages
            all_evaluation_scores.append(float(evaluation))
            all_response_times.append(response["response_time"])
            all_completion_tokens.append(response["completion_tokens"])
            all_total_tokens.append(response["total_tokens"])

            # Collect data for CSV
            csv_data.append({
                'question_number': i,
                'test_number': j+1,
                'model_name': subject_model,
                'evaluator': evaluator,
                'evaluator_model': evaluator_model,
                'prompt_tokens': response["prompt_tokens"],
                'completion_tokens': response["completion_tokens"],
                'total_tokens': response["total_tokens"],
                'response_time': f"{response['response_time']:.2f}",
                'evaluation_score': f"{float(evaluation):.2f}"
            })

        # Calculate per-question averages
        avg_score = statistics.mean(question_evaluation_scores)
        avg_question_response_time = statistics.mean(question_response_times)
        avg_question_completion_tokens = statistics.mean(question_completion_tokens)
        avg_question_total_tokens = statistics.mean(question_total_tokens)

        print("=" * 50)
        print(f"Question {i} Averages:")
        print(f"  Score: {avg_score:.2f}")
        print(f"  Response Time: {avg_question_response_time:.2f} seconds")
        print(f"  Completion Tokens: {avg_question_completion_tokens:.2f}")
        print(f"  Total Tokens: {avg_question_total_tokens:.2f}")

        # Add per-question averages row to CSV data
        csv_data.append({
            'question_number': i,
            'test_number': 'Average',
            'model_name': '',
            'evaluator': '',
            'evaluator_model': '',
            'prompt_tokens': '',
            'completion_tokens': f"{avg_question_completion_tokens:.2f}",
            'total_tokens': f"{avg_question_total_tokens:.2f}",
            'response_time': f"{avg_question_response_time:.2f}",
            'evaluation_score': f"{avg_score:.2f}"
        })

    # Calculate overall averages
    avg_evaluation_score = statistics.mean(all_evaluation_scores)
    avg_response_time = statistics.mean(all_response_times)
    avg_completion_tokens = statistics.mean(all_completion_tokens)
    avg_total_tokens = statistics.mean(all_total_tokens)

    # Add overall averages row to CSV data
    csv_data.append({
        'question_number': 'Overall',
        'test_number': 'Average',
        'model_name': '',
        'evaluator': '',
        'evaluator_model': '',
        'prompt_tokens': '',
        'completion_tokens': f"{avg_completion_tokens:.2f}",
        'total_tokens': f"{avg_total_tokens:.2f}",
        'response_time': f"{avg_response_time:.2f}",
        'evaluation_score': f"{avg_evaluation_score}"
    })

    # Write to CSV file
    with open('test_results.csv', 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['question_number', 'test_number', 'model_name', 'evaluator', 'evaluator_model', 'prompt_tokens', 'completion_tokens', 'total_tokens', 'response_time', 'evaluation_score']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(csv_data)

    print(f"\nResults exported to test_results.csv")

    # Print overall averages to console
    print("=" * 50)
    print("OVERALL AVERAGES:")
    print(f"Average Score: {avg_evaluation_score:.2f}")
    print(f"Average Response Time: {avg_response_time:.2f} seconds")
    print(f"Average Completion Tokens: {avg_completion_tokens:.2f}")
    print(f"Average Total Tokens: {avg_total_tokens:.2f}")
    print("=" * 50)


if __name__ == "__main__":
    main()