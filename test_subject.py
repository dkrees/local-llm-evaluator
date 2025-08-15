import time
from providers.anthropic import call_anthropic_model
from providers.lmstudio import call_lmstudio_model
from providers.openai import call_openai_model
from evaluators.evaluation_types import EvaluationType

def test_model(provider:str, model:str="*", evaluation_type:EvaluationType = None, question:str = "", temperature=0.5):

  instructions = ""

  if evaluation_type == EvaluationType.RATIONALE:
    instructions = "Answer the questions accurately. Provide your rationale where possible."
  elif evaluation_type == EvaluationType.SIMPLE_QUESTION:
    instructions = "Answer the question with a short, accurate response."
  elif evaluation_type == EvaluationType.SUMMARISE:
    instructions = "Summarise the given text, maintain the key and factual elements."

  # Start a timer for the local model completion
  start_time = time.time()

  if provider == 'openai':
    response = call_openai_model(model, instructions, question, temperature)
  elif provider == 'anthropic':
    response = call_anthropic_model(model, instructions, question, temperature)
  elif provider == 'lmstudio':
    response = call_lmstudio_model(model, instructions, question, temperature)
  else:
    response = call_lmstudio_model(model, instructions, question, temperature)

  # End time and response time
  end_time = time.time()
  response_time = end_time - start_time

  return {
    "response": response["response"],
    "response_time": response_time,
    "prompt_tokens": response["prompt_tokens"],
    "completion_tokens": response["completion_tokens"],
    "total_tokens": response["total_tokens"]
  }