import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def call_openai_model(model, system_prompt, prompt, temperature=0.2, max_output_tokens=200):
  try:
    response = client.responses.create(
      model=model,
      instructions=system_prompt,
      input=prompt,
      temperature=temperature,
      max_output_tokens=max_output_tokens
    )
    return response.output[0].content[0].text

  except Exception as e:
    return f"Error: {e}"