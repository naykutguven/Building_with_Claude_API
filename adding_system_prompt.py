from dotenv import load_dotenv
load_dotenv()

from anthropic import Anthropic

client = Anthropic()  # picks up ANTHROPIC_API_KEY automatically
model = "claude-haiku-4-5"

def chat(messages, system=None):
    params = {
        "model": model,
        "max_tokens": 1000,
        "messages": messages,
    }
    
    if system:
        params["system"] = system
    
    message = client.messages.create(**params)
    return message.content[0].text

# Example usage with a system prompt
messages = [{"role": "user", "content": "How do I solve 5x + 3 = 0."}]
system = """
You are a patient math tutor.
Do not directly answer a student's questions.
Guide them to a solution step by step.
"""
answer = chat(messages, system=system)
print(answer)