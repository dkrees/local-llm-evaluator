from providers.anthropic import call_anthropic_model
from providers.openai import call_openai_model
from providers.lmstudio import call_lmstudio_model

def evaluate(evaluator, evaluator_model, question, answer, expected_answer):

    temperature = 0.2
    max_output_tokens = 200

    system_prompt = f"""
    You are an expert evaluator specialising in assessing answer accuracy.
    Focus only on comparing the given answer to the expected answer.
    Ignore formatting, style, or extra information unless it affects correctness.
    You must respond with a numeric score of either 0 or 1 only.
    """

    prompt = f"""
    Please evaluate the ANSWER to a QUESTION by comparing it to the EXPECTED ANSWER:

    **Rating Scale:**
    - 1: Correct answer
    - 0: Incorrect answer

    **Evaluation Criteria:**
    - **Correctness**: Does the answer match the expected answer exactly?

    ORIGINAL QUESTION:
    {question}

    EXPECTED ANSWER:
    {expected_answer}

    ANSWER TO EVALUATE:
    {answer}

    Respond with the numeric score only.
    """

    if (evaluator == 'lmstudio'):
        response = call_lmstudio_model(evaluator_model, system_prompt, prompt, temperature)
        evaluation_text = response["response"]
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

