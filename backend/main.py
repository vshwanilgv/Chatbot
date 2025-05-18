from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import google.generativeai as genai
import uuid
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GENAI_API_KEY")
genai.configure(api_key=api_key)  

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
models = genai.list_models()

# for m in models:
#     print(f"{m.name} - supports generateContent: {'generateContent' in m.supported_generation_methods}")


chat_sessions = {}

class ChatRequest(BaseModel):
    message: str
    session_id: str = None

@app.post("/chat")
def chat(req: ChatRequest):
    session_id = req.session_id or str(uuid.uuid4())

    if session_id not in chat_sessions:
        model = genai.GenerativeModel("models/gemini-1.5-pro-latest")
        chat_sessions[session_id] = model.start_chat(history=[])
    
    chat = chat_sessions[session_id]
    response = chat.send_message(req.message)

    return {"reply": response.text, "session_id": session_id}
