from providers.anthropic import call_anthropic_model
from providers.openai import call_openai_model

def evaluate(evaluator, evaluator_model, question, answer, expected_answer):

    temperature = 0.2
    max_output_tokens = 200

    system_prompt = "You are an expert evaluator specialising in assessing answer accuracy. Focus solely on comparing the given answer to the expected answer. Ignore formatting, style, or extra information unless it affects correctness. You must respond with a numeric score between 0.0 and 1.0, followed by a pipe symbol (|), then a brief one-sentence reasoning for your evaluation."

    prompt = f"""
    Please evaluate the ANSWER to a QUESTION by comparing it to the EXPECTED ANSWER. Assess the correctness of the answer. Rate from 0.0 to 1.0:

    **Rating Scale:**
    - 1.0: Correct answer
    - 0.0: Incorrect answer

    **Evaluation Criteria:**
    - **Correctness**: Does the answer match the expected answer?

    ORIGINAL QUESTION:
    {question}

    EXPECTED ANSWER:
    {expected_answer}

    ANSWER TO EVALUATE:
    {answer}

    Provide the numeric score followed by a pipe symbol and brief reasoning (e.g. "1.0|The answer correctly identifies three ducks as the solution to the logic puzzle.").
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

