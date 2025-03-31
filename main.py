from fastapi import FastAPI
from pydantic import BaseModel
import requests

app = FastAPI()

class Message(BaseModel):
    user_input: str

@app.post("/chat")
def chat(msg: Message):
    url = "https://api.intelligence.io.solutions/api/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer io-v2-eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJvd25lciI6ImI4OTczMjQzLTJiOGUtNGViMi05ZGI2LTQ2ZTAyZGM4Zjg2ZSIsImV4cCI6NDg5Njk3NjE4Nn0.LHeUGbvIvfnrunZup8r4a7Z8DmiP88hNeDZSBmq5oRUmyOnkaHLP4TcyIUIaJ7McM7ad21XEt2SgVfFU8T6zPw",
    }
    data = {
        "model": "deepseek-ai/DeepSeek-R1",
        "messages": [
            {"role": "system", "content": "You are a helpful assistant"},
            {"role": "user", "content": msg.user_input}
        ],
    }
    response = requests.post(url, headers=headers, json=data)
    content = response.json()['choices'][0]['message']['content']
    return {"response": content.split('</think>\n\n')[1]}

