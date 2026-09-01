import os

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI


def main():
    load_dotenv()

    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0
    )

    prompt = "Explain what Kubernetes is in three simple points."

    response = llm.invoke(prompt)

    print("\nAI Response:")
    print(response.content)


if __name__ == "__main__":
    main()