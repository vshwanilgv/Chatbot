# backend/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import google.generativeai as genai
import uuid
import os

# Load your Gemini API Key
genai.configure(api_key="your-gemini-api-key")  # Replace with your key

app = FastAPI()

# Allow frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

chat_sessions = {}

class ChatRequest(BaseModel):
    message: str
    session_id: str = None

@app.post("/chat")
def chat(req: ChatRequest):
    session_id = req.session_id or str(uuid.uuid4())

    if session_id not in chat_sessions:
        model = genai.GenerativeModel("gemini-pro")
        chat_sessions[session_id] = model.start_chat(history=[])
    
    chat = chat_sessions[session_id]
    response = chat.send_message(req.message)

    return {"reply": response.text, "session_id": session_id}
