# import os
from openai import OpenAI
# from dotenv import load_dotenv

# load_dotenv()
# client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
client = OpenAI(base_url="http://127.0.0.1:1234/v1", api_key="*")

def call_lmstudio_model(model, system_prompt, prompt, temperature=0.5):
  try:
    response = client.chat.completions.create(
      model=model,
      messages=[
          {"role": "system", "content": f"{system_prompt}"},
          {"role": "user", "content": prompt}
      ],
      temperature=temperature,
    )
    return {
      "response": response.choices[0].message.content,
      "prompt_tokens": response.usage.prompt_tokens,
      "completion_tokens": response.usage.completion_tokens,
      "total_tokens": response.usage.total_tokens
    }

  except Exception as e:
    raise e