import os
import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav
import librosa
import torch
import logging
from datetime import datetime
from transformers import WhisperProcessor, WhisperForConditionalGeneration

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

processor = WhisperProcessor.from_pretrained("openai/whisper-medium.en")
model = WhisperForConditionalGeneration.from_pretrained("openai/whisper-medium.en")


SAMPLE_RATE = 16000  
ASR_DIR = "asr"

os.makedirs(ASR_DIR, exist_ok=True)


def record_and_transcribe(duration=5):
    """
    Records audio from the microphone, saves it to the `asr/` directory, and returns the Whisper transcription.
    """
    try:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = os.path.join(ASR_DIR, f"recorded_audio_{timestamp}.wav")

        logger.info(f"🎙️ Starting recording for {duration} seconds...")
        audio = sd.rec(int(duration * SAMPLE_RATE), samplerate=SAMPLE_RATE, channels=1, dtype='float32')
        sd.wait()
        wav.write(filename, SAMPLE_RATE, (audio * 32767).astype(np.int16))
        logger.info(f"Recording saved as {filename}")

        logger.info("Loading and processing audio...")
        audio_array, sampling_rate = librosa.load(filename, sr=SAMPLE_RATE)
        inputs = processor(audio_array, sampling_rate=sampling_rate, return_tensors="pt", padding=True)
        input_features = inputs.input_features
        attention_mask = inputs.get("attention_mask", None)

        logger.info("Running transcription with Whisper model...")
        with torch.no_grad():
            predicted_ids = model.generate(input_features, attention_mask=attention_mask)

        transcription = processor.batch_decode(predicted_ids, skip_special_tokens=True)[0]
        logger.info("Transcription completed successfully.")
        return transcription

    except Exception as e:
        logger.error(f"Error during recording/transcription: {e}", exc_info=True)
        return "Transcription failed due to an error."
    
    finally:
        if filename and os.path.exists(filename):
            try:
                os.remove(filename)
                logger.info(f"Temporary audio file {filename} deleted.")
            except Exception as cleanup_error:
                logger.warning(f"Could not delete temporary file {filename}: {cleanup_error}")


