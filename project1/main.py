import os
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI

# Load API key and base from .env

load_dotenv()
api_key = os.environ.get("OPENAI_API_KEY")
api_base = os.environ.get("OPENAI_API_BASE", "https://openrouter.ai/api/v1")  # default if not set

if not api_key:
    raise ValueError("OPENAI_API_KEY not found in .env")

# Set environment variables for OpenRouter
os.environ["OPENAI_API_KEY"] = api_key
os.environ["OPENAI_API_BASE"] = api_base


# Create the AI model

llm = ChatOpenAI(
    model="gpt-4o-mini",   # OpenRouter model
    temperature=0
)


# Main chat loop

def main():
    print("\nWelcome! I'm your AI Assistant. Type 'quit' to exit.")
    print("You can chat normally or type math like 'add 4 into 7'.")

    while True:
        user_input = input("\nYou: ").strip()
        if user_input.lower() == "quit":
            print("Goodbye!")
            break

        # Send input to the AI model
        response = llm.generate([[HumanMessage(content=user_input)]])

        # Pylance-friendly: use gen.text instead of gen.message.content
        assistant_text = ""
        for gen_list in response.generations:
            for gen in gen_list:
                assistant_text += str(gen.text)

        print("\nAssistant:", assistant_text)


if __name__ == "__main__":
    main()