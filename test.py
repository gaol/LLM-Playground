#!/bin/python

import os

pp = os.environ.get("PYTHONPATH")
print(f"{pp}")


from llms import llm

# initialize the LLM provider
llms = llm.LLMProviderRegistry()
llms.load_from_default()

model_name = "DEEPSEEK-CHAT"
llm_handler = llms.get_llm_handler(model_name)
if llm_handler is None:
    print(f"Model with name: {model_name} is not defined.")
    exit(1)

prompt = "Please list 10 English words relating to food, returns only the words list, one word per line."
words_list = llm_handler.chat(prompt)
print(f"English Words List: {words_list}")
