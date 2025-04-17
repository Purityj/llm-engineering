import requests, subprocess
from bs4 import BeautifulSoup

# Methods of connecting to Ollama 
# 1. connecting to Ollama directly using Ollama API
OLLAMA_API="http://localhost:11434/api/chat"
HEADERS={"Content-Type": "application/json"}
MODEL="llama3.2"

messages = [
    {"role": "user", "content": "Describe some of the applications of Generative AI"}
]

payload = {
    "model": MODEL,
    "messages": messages,
    "stream": False,
}

subprocess.run(["ollama", "pull", MODEL], check=True)  # downloads the model if its not already downloaded

response = requests.post(OLLAMA_API, json=payload, headers=HEADERS)
print(response.status_code)
print(response.json()['message']['content'])

# 2. using OpenAI python library to connect to Ollama
from openai import OpenAI
ollama_via_openai = OpenAI(base_url='http://localhost:11434/v1', api_key='ollama')

response = ollama_via_openai.chat.completions.create(
    model=MODEL,
    messages=messages,
    )
print(response.choices[0].message.content)

