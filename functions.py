from openai import OpenAI

client = OpenAI(base_url="http://127.0.0.1:1234/v1", api_key="*")

history = [
    {"role": "system", "content": "You are an intelligent assistant, you will always provide helpful and factual answers to questions."},
    {"role": "user", "content": "Introduce yourself. Be humorous but short and concise."}
]

def main():
    while True:
        completion = client.chat.completions.create(
            model="mistralai/mistral-small-3.2",
            messages=history,
            temperature=0.7,
            stream=True
        )

        new_message = {"role": "assistant", "content": "x"}

        for chunk in completion:
            if chunk.choices[0].delta.content:
                print(chunk.choices[0].delta.content, end="", flush=True)
                new_message["content"] += chunk.choices[0].delta.content
        
        history.append(new_message)
        print("")
        history.append({"role": "user", "content": input(">> ")})


if __name__ == "__main__":
    main()