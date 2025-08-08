import os
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()
client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

def call_anthropic_model(model, system_prompt, prompt, temperature=0.2, max_output_tokens=200):
  try:
    response = client.messages.create(
      model=model,
      system=system_prompt,
      messages=[
          {"role": "user", "content": prompt}
      ],
      temperature=temperature,
      max_tokens=max_output_tokens
    )

    return response.content[0].text

  except Exception as e:
    return f"Error: {e}"