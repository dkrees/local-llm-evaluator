from openai import OpenAI

client = OpenAI(base_url="http://127.0.0.1:1234/v1", api_key="*")

completion = client.chat.completions.create(
    model="mistralai/mistral-small-3.2",
    messages=[
        {"role": "system", "content": "You are an expert Solution Architect"},
        {"role": "user", "content": "I want you to create an example of Architectural Decision Record for the selection of a database."}
    ],
    temperature=0.7
)

def main():
    print("Hello, World!")
    print("Your python app is running!")
    print(completion.choices[0].message.content)

if __name__ == "__main__":
    main()