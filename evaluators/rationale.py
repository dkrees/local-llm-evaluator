from model_openai import call_openai_model
from model_anthropic import call_anthropic_model

def evaluate(evaluator, evaluator_model, question, answer, expected_answer):

    temperature = 0.2
    max_output_tokens = 200

    system_prompt = "You are an expert evaluator specialising in assessing answer accuracy and reasoning quality. Focus solely on comparing the given answer to the expected answer. Ignore formatting, style, or extra information unless it affects correctness. You must respond only with a numeric score between 0.0 and 1.0. Do not provide any further comments or text."

    prompt = f"""
    Please evaluate the ANSWER to a QUESTION by comparing it to the EXPECTED ANSWER. Assess both correctness and quality of reasoning. Rate from 0.0 to 1.0:

    **Rating Scale:**
    - 1.0: Correct answer with excellent, logical, and accurate rationale
    - 0.8: Correct answer with good rationale that may have minor gaps or unclear elements
    - 0.6: Correct answer with poor, missing, or inaccurate rationale
    - 0.4: Incorrect answer with well-constructed but fundamentally flawed rationale
    - 0.2: Incorrect answer with poor or mostly inaccurate rationale
    - 0.0: Incorrect answer with no rationale or completely inaccurate reasoning

    **Evaluation Criteria:**
    - **Correctness**: Does the answer match the expected answer?
    - **Rationale Quality**: Is the reasoning logical, accurate, and well-explained?

    ORIGINAL QUESTION:
    {question}

    EXPECTED ANSWER:
    {expected_answer}

    ANSWER TO EVALUATE:
    {answer}

    Provide only the numeric score (e.g. 0.8).
    """

    if (evaluator == 'openai'):
        response = call_openai_model(evaluator_model, system_prompt, prompt, temperature, max_output_tokens)
        return response
    elif (evaluator == 'anthropic'):
        response = call_anthropic_model(evaluator_model, system_prompt, prompt, temperature, max_output_tokens)
        return response

