from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from memory.search import create_final_message 

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class PromptInput(BaseModel):
    prompt: str

@app.post("/remix")
async def remix_prompt(payload: PromptInput):
    compiled = create_final_message(payload.prompt)
    return {"compiled_message": compiled}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5000)
