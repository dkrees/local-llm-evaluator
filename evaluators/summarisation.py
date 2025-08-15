from providers.anthropic import call_anthropic_model
from providers.openai import call_openai_model

def evaluate(evaluator, evaluator_model, question, answer, expected_answer=None):

    temperature = 0.2
    max_output_tokens = 200

    system_prompt = f"""
    You are an expert evaluator specialising in assessing text summarisation quality.
    Focus on factual accuracy, completeness of key information, clarity, structure, and appropriate length.
    Ignore minor formatting or stylistic preferences unless they significantly impact comprehension.
    You must respond with a numeric score between 0.0 and 1.0, followed by a pipe symbol (|), then a brief one-sentence reasoning for your evaluation.
    """

    prompt = f"""
    Please evaluate the provided SUMMARISATION against the original TEXT. Assess factual accuracy, retention of key information, clarity, structure, and appropriate length. Rate from 0.0 to 1.0.
    Clearly identify the actual summarised text to evaluate, seperating and ingoring any thought and reasoning processes, for example any text between "<think> </think>" tags. Only evaluate the summary text.

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

    Provide the numeric score followed by a pipe symbol and brief reasoning (e.g. "0.9|Excellent summary with accurate facts and good structure, but slightly verbose.").
    """

    if (evaluator == 'openai'):
        response = call_openai_model(evaluator_model, system_prompt, prompt, temperature, max_output_tokens)
        evaluation_text = response["response"]
    elif (evaluator == 'anthropic'):
        response = call_anthropic_model(evaluator_model, system_prompt, prompt, temperature, max_output_tokens)
        evaluation_text = response["response"]
    
    # Parse the response to extract score and reasoning
    try:
        if '|' in evaluation_text:
            score, reasoning = evaluation_text.split('|', 1)
            return {'score': score.strip(), 'reasoning': reasoning.strip()}
        else:
            # Fallback if no pipe delimiter found
            return {'score': evaluation_text.strip(), 'reasoning': 'No reasoning provided'}
    except:
        return {'score': '0.0', 'reasoning': 'Error parsing evaluation response'}

