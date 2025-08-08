from model_openai import call_openai_model
from model_anthropic import call_anthropic_model

def evaluate(evaluator, evaluator_model, question, answer, expected_answer=None):

    temperature = 0.2
    max_output_tokens = 200

    system_prompt = f"""
    You are an expert evaluator specialising in assessing text summarisation quality.
    Focus on factual accuracy, completeness of key information, clarity, structure, and appropriate length.
    Ignore minor formatting or stylistic preferences unless they significantly impact comprehension.
    Respond only with a numeric score between 0.0 and 1.0.
    """

    prompt = f"""
    Please evaluate the provided SUMMARISATION against the original TEXT. Assess factual accuracy, retention of key information, clarity, structure, and appropriate length. Rate from 0.0 to 1.0:

    **Rating Scale:**
    - 1.0: Factually accurate, captures all key information, excellently structured and clear, optimal length
    - 0.8: Factually accurate, captures most key information, well-structured and clear, appropriate length
    - 0.6: Mostly accurate with minor factual errors, captures some key information, adequately structured, reasonable length
    - 0.4: Some factual errors, misses several key points, poorly structured or unclear, inappropriate length (too long/short)
    - 0.2: Multiple factual errors, misses most key information, very poor structure, significantly inappropriate length
    - 0.0: Major factual inaccuracies, fails to capture key information, incoherent structure, completely inappropriate length


    **Evaluation Criteria:**
    - **Factual Accuracy**: Are all facts and details correctly represented?
    - **Key Information Retention**: Are the most important points from the original text included?
    - **Clarity and Structure**: Is the summary well-organised and easy to understand?
    - **Appropriate Length**: Is the summary suitably concise whilst retaining essential information?

    ORIGINAL QUESTION:
    {question}

    SUMMARISATION TO EVALUATE:
    {answer}

    Provide only the numeric score (e.g. 1.0).
    """

    if (evaluator == 'openai'):
        response = call_openai_model(evaluator_model, system_prompt, prompt, temperature, max_output_tokens)
        return response
    elif (evaluator == 'anthropic'):
        response = call_anthropic_model(evaluator_model, system_prompt, prompt, temperature, max_output_tokens)
        return response

