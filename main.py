from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests
import os


app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://moonlit-paprenjak-6f5c38.netlify.app"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Message(BaseModel):
    user_input: str


@app.post("/chat")
def chat(msg: Message):
    api_key = os.environ.get("DEEPSEEK_API_KEY")
    if not api_key:
        return {"error": "API key is missing. Set DEEPSEEK_API_KEY environment variable."}

    url = "https://api.intelligence.io.solutions/api/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
    }

    data = {
        "model": "deepseek-ai/DeepSeek-R1",
        "messages": [
            {"role": "system", "content": "You are ai instrument wich change and improve text .U only need to improve text "},
            {"role": "user", "content": msg.user_input}
        ],
    }

    response = requests.post(url, headers=headers, json=data)

    try:
        content = response.json()['choices'][0]['message']['content']
        return {"response": content.split('</think>\n\n')[1]}
    except Exception as e:
        return {"error": "Failed to parse DeepSeek response", "details": str(e)}
