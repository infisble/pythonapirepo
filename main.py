from fastapi import FastAPI
from pydantic import BaseModel
import requests
import os

app = FastAPI()

class Message(BaseModel):
    user_input: str

@app.post("/chat")
def chat(msg: Message):
    api_key = os.environ.get("DEEPSEEK_API_KEY")  # читаем из переменных окружения
    if not api_key:
        return {"error": "API ключ не найден. Установите переменную окружения DEEPSEEK_API_KEY"}

    url = "https://api.intelligence.io.solutions/api/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
    }
    data = {
        "model": "deepseek-ai/DeepSeek-R1",
        "messages": [
            {"role": "system", "content": "You are a helpful assistant which can only update text wich are profesional summary wich now i write"},
            {"role": "user", "content": msg.user_input}
        ],
    }
    response = requests.post(url, headers=headers, json=data)
    content = response.json()['choices'][0]['message']['content']
    return {"response": content.split('</think>\n\n')[1]}
