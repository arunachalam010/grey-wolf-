from fastapi import FastAPI
from pydantic import BaseModel
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

app = FastAPI()

# Model state
is_online = False
model = None
tokenizer = None

model_name = "deepseek-ai/deepseek-coder-1.3b"

class RequestData(BaseModel):
    chat_history: list[str]

@app.post("/generate")
async def generate_text(data: RequestData):
    if not is_online:
        return {"response": "🔴 Model is offline. Please turn it ON."}
    
    conversation = " ".join(data.chat_history)
    input_ids = tokenizer.encode(conversation, return_tensors="pt").to("cuda")

    output = model.generate(input_ids, max_length=300)
    response = tokenizer.decode(output[0], skip_special_tokens=True)

    return {"response": response}

@app.get("/status")
def get_status():
    return {"status": "online" if is_online else "offline"}

@app.post("/toggle")
def toggle_model():
    global is_online, model, tokenizer

    if is_online:
        is_online = False
        model, tokenizer = None, None  # Unload model
    else:
        is_online = True
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        model = AutoModelForCausalLM.from_pretrained(model_name, torch_dtype=torch.float16, device_map="auto")
    
    return {"status": "online" if is_online else "offline"}

