import random

import requests

API_URL = "https://api-inference.huggingface.co/models/mistralai/Mixtral-8x7B-Instruct-v0.1"
headers = {"Authorization": "Bearer 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"}

RNG = random.randint(1,1000000);

def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()


output = query({
    "inputs": "What is a list of restaurants in belfast? (Return as a bulletpoint list of only names and addresses.)",
    "max_new_tokens": 100,
    "return_full_text": False,
    "seed": RNG,
    "temperature": 0.5,
})

print(output[0]['generated_text'])

