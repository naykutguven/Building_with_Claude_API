from dotenv import load_dotenv
load_dotenv()

from anthropic import Anthropic
from pydantic import BaseModel

import json

client = Anthropic()  # picks up ANTHROPIC_API_KEY automatically
model = "claude-sonnet-5-5"

class Task(BaseModel):
    task: str

class Dataset(BaseModel):
    tasks: list[Task]

def add_user_message(messages, text):
    user_message = {"role": "user", "content": text}
    messages.append(user_message)

def add_assistant_message(messages, text):
    assistant_message = {"role": "assistant", "content": text}
    messages.append(assistant_message)

def chat(messages, system=None, stop_sequences=[], output_format=None):
    params = {
        "model": model,
        "max_tokens": 16000,  # room for thinking, which is on by default on Sonnet 5.5
        "messages": messages,
        # if a request is declined by a safety classifier, retry it on a fallback model
        "betas": ["server-side-fallback-2026-07-01"],
        "fallbacks": "default",
    }
    if system:
        params["system"] = system
    if stop_sequences:
        params["stop_sequences"] = stop_sequences

    if output_format:
        # structured outputs: the reply is guaranteed to match the Pydantic model's schema
        response = client.beta.messages.parse(**params, output_format=output_format)
        if response.stop_reason != "end_turn" or response.parsed_output is None:
            raise RuntimeError(f"No structured output (stop_reason: {response.stop_reason})")
        return response.parsed_output

    response = client.beta.messages.create(**params)
    # response.content can start with a thinking block, so pick out the text
    return "".join(block.text for block in response.content if block.type == "text")

def generate_dataset():
    prompt = """
Generate an evaluation dataset for a prompt evaluation. The dataset will be used to evaluate prompts that generate Python, JSON, or Regex specifically for AWS-related tasks. Generate a list of tasks, each requiring Python, JSON, or a Regex to complete.

* Focus on tasks that can be solved by writing a single Python function, a single JSON object, or a single regex
* Focus on tasks that do not require writing much code

Please generate 3 tasks.
"""

    messages = []
    add_user_message(messages, prompt)
    return chat(messages, output_format=Dataset)

# only generate the dataset when this file is run directly, not when another lesson imports chat() from it
if __name__ == "__main__":
    dataset = generate_dataset()
    print(dataset.model_dump_json(indent=2))

    # model_dump() turns the Pydantic objects into plain dicts that json can write;
    # save just the list of tasks so the file is a JSON array
    with open('dataset.json', 'w') as f:
        json.dump(dataset.model_dump()["tasks"], f, indent=2)
