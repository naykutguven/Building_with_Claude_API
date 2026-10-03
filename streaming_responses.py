from dotenv import load_dotenv
load_dotenv()

from anthropic import Anthropic

client = Anthropic()  # picks up ANTHROPIC_API_KEY automatically
model = "claude-haiku-4-5"

def add_user_message(messages, text):
    user_message = {"role": "user", "content": text}
    messages.append(user_message)

def add_assistant_message(messages, text):
    assistant_message = {"role": "assistant", "content": text}
    messages.append(assistant_message)

def chat(messages):
    message = client.messages.create(
        model=model,
        max_tokens=1000,
        messages=messages,
    )
    return message.content[0].text

messages = []
add_user_message(messages, "Write a 1 sentence description of a fake database")

# stream = client.messages.create(
#     model=model,
#     max_tokens=1000,
#     messages=messages,
#     stream=True
# )

# for event in stream:
#     print(event)


# Or we can use the SDK's streaming interface to handle responses in real-time.
# This approach automatically filters out everything except the actual text content, 
# which is usually what you need for displaying responses to users.

with client.messages.stream(
    model=model,
    max_tokens=1000,
    messages=messages,
) as stream:
    for event in stream:
        print(event)

    # Get the complete message for database storage
    final_message = stream.get_final_message()