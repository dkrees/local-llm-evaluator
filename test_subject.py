import time
from openai import OpenAI
from evaluators.evaluation_types import EvaluationType

client = OpenAI(base_url="http://127.0.0.1:1234/v1", api_key="*")

def test_model(model:str="*", evaluation_type:EvaluationType = None, question:str = "", temperature=0.5):

  instructions = ""

  if evaluation_type == EvaluationType.RATIONALE:
    instructions = "Answer the questions accurately. Provide your rationale where possible."
  elif evaluation_type == EvaluationType.SIMPLE_QUESTION:
    instructions = "Answer the question with a short accurate response."
  elif evaluation_type == EvaluationType.SUMMARISE:
    instructions = "Summarise the given text, maintain the key and factual elements."


  # Start a timer for the local model completion
  start_time = time.time()

  # Call the local model
  completion = client.chat.completions.create(
      model=model, # Must specify the model when multiple models are loaded in LMStudio
      messages=[
          {"role": "system", "content": f"{instructions}"},
          {"role": "user", "content": question}
      ],
      temperature=temperature
  )

  # End time and response time
  end_time = time.time()
  response_time = end_time - start_time

  return {
    "response": completion.choices[0].message.content,
    "response_time": response_time,
    "prompt_tokens": completion.usage.prompt_tokens,
    "completion_tokens": completion.usage.completion_tokens,
    "total_tokens": completion.usage.total_tokens
  }