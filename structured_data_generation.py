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

def chat(messages, stop_sequences=None):
    params = {
        "model": model,
        "max_tokens": 1000,
        "messages": messages,
    }
    
    if stop_sequences is not None:
        params["stop_sequences"] = stop_sequences
     
    message = client.messages.create(**params)
    return message.content[0].text

# Suppose you want to generate structured data from a user prompt and ask Claude to
# generate an AWS EventBridge rule.
# By default, when you ask Claude to generate JSON, you might get something like this
# (complete response in markdown format) and also adds some explanatory comments:

# ```json
# \{
#   "source": ["aws.ec2"],
#   "detail-type": ["EC2 Instance State-change Notification"],
#   "detail": \{
#     "state": ["running"]
#   \}
# \}
# ```
#
# This rule captures EC2 instance state changes when instances start running.

# But we don't want the response to be in markdown format; we just want the raw JSON.
#
# For that, we can use "assistant message prefilling" and "stop sequences"


messages = []

add_user_message(messages, "Generate a very short event bridge rule as json")
add_assistant_message(messages, "```json")

text = chat(messages, stop_sequences=["```"])