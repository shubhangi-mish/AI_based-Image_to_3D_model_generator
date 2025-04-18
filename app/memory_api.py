from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import logging
from memory.search import create_final_message
from asr.speech2txt import record_and_transcribe


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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

class AudioRequest(BaseModel):
    duration: int = 5  

# Endpoints
@app.post("/remix")
async def remix_prompt(payload: PromptInput):
    logger.info(f"Received remix prompt: {payload.prompt}")
    compiled = create_final_message(payload.prompt)
    return {"compiled_message": compiled}

@app.post("/record_and_transcribe/")
async def record_and_transcribe_api(request: AudioRequest):
    """
    Records audio using the microphone and returns the Whisper transcription.
    """
    logger.info(f"API request received to record audio for {request.duration} seconds.")
    transcription = record_and_transcribe(duration=request.duration)
    return {"transcription": transcription}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5000)
