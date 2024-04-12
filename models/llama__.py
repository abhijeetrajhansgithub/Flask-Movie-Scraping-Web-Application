import json
from llamaapi import LlamaAPI


def run_nlp(prompt):
    print("inside MODEL, prompt: ", prompt)
    # Initialize the SDK
    llama = LlamaAPI("API_KEY")

    # initial_prompt = "You are a review summarizer. Summarize the following review(s) into one single paragraph: "
    # prompt = initial_prompt + prompt

    # Build the API request
    api_request_json = {
        "messages": [
            {"role": "user", "content": f"{prompt}"},
        ],
        "stream": False,
        "function_call": "get_current_weather",
    }

    # Execute the Request
    response = llama.run(api_request_json)
    response = response.json()

    content = response["choices"][0]["message"]["content"]
    print(content)

    return content

