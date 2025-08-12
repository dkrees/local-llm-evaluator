import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def call_openai_model(model, system_prompt, prompt, temperature=0.2, max_output_tokens=4000):
  try:
    response = client.chat.completions.create(
      model=model,
      messages=[
          {"role": "system", "content": system_prompt},
          {"role": "user", "content": prompt}
      ],
      temperature=temperature,
      max_tokens=max_output_tokens
    )
    return {
      "response": response.choices[0].message.content,
      "prompt_tokens": response.usage.prompt_tokens,
      "completion_tokens": response.usage.completion_tokens,
      "total_tokens": response.usage.total_tokens
    }

  except Exception as e:
    raise e