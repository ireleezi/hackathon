import os

from openai import OpenAI
#TODO Should be pulled from env value but im shite and couldnt get it working and this project is supposed to be minimal amount of work
client = OpenAI(api_key="")
completion = client.chat.completions.create(
    model="gpt-4",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {
            "role": "user",
            "content": "Write a haiku about recursion in programming."
        }
    ]
)

print(completion.choices[0].message)