from fastapi import FastAPI, HTTPException
import aiohttp
import asyncio
from pydantic import BaseModel
import os
from dotenv import load_dotenv

load_dotenv()
RAPID_API_KEY = os.getenv('RAPID_API_KEY')

app = FastAPI()

def format_answer(answer):
    # Basic formatting can be expanded based on specific needs
    return answer.replace(" '", "'").replace(" ,", ",").replace(" .", ".").replace(" -", "-")

class AIRequest(BaseModel):
    prompt: str

async def send_post_request(url, json_data, headers):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=json_data, headers=headers) as response:
                if 'application/json' in response.headers.get('Content-Type', ''):
                    return await response.json()
                else:
                    return await response.text()
    except aiohttp.ClientConnectorError as e:
        raise HTTPException(status_code=500, detail=f"Connection error: {e}")

@app.post("/generate-ai-response/")
async def generate_ai_response(request: AIRequest):
    url = "https://meta-llama-fast-api.p.rapidapi.com/mistralchat"
    payload = {"message": request.prompt}
    headers = {
        "Content-Type": "application/json",
        "X-RapidAPI-Key": RAPID_API_KEY,  # Replace with your actual RapidAPI key
        "X-RapidAPI-Host": "meta-llama-fast-api.p.rapidapi.com"
    }

    response = await send_post_request(url, payload, headers)
    print(f'{response  = } llama')
    return response

import uvicorn

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", 8000)))