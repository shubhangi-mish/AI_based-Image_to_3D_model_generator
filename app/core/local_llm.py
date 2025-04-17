import logging
from llama_cpp import Llama
from huggingface_hub import hf_hub_download

model_path = hf_hub_download(
    repo_id="TheBloke/TinyLlama-1.1B-Chat-v1.0-GGUF",
    filename="tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf"
)

llm = Llama(
    model_path=model_path,
    n_ctx=2048,
    n_gpu_layers=-1
)

def run_local_llm(prompt: str, system_prompt: str = "You are a helpful AI assistant who creates very vivid prompts for creating images from the user query") -> str:

    logging.info(f"Running local LLM with prompt: {prompt}")

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": prompt}
    ]

    try:
        response = llm.create_chat_completion(
            messages=messages,
            max_tokens=512,
            temperature=0.7,
            stop=["User:", "<|im_end|>"]
        )

        content = response['choices'][0]['message']['content']
        logging.info(f"LLM Response: {content}")
        return content

    except Exception as e:
        logging.exception("LLM Error")
        return "An error occurred while generating the response."
