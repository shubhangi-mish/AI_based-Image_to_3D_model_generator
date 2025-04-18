import os
import logging
import json
from pinecone import Pinecone
from dotenv import load_dotenv
import os

logging.basicConfig(level=logging.INFO)

load_dotenv()

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_HOST = os.getenv("PINECONE_HOST")

INDEX_NAME = "openfabric"
NAMESPACE = "default"

pc = Pinecone(api_key=PINECONE_API_KEY)
index = pc.Index(INDEX_NAME, host=PINECONE_HOST)

def query_vector_db(user_prompt: str) -> str:
    """
    Query Pinecone vector database to find the most similar prompt to the user's input.
    Returns the qid of the most similar prompt.
    """
    logging.info(f"Querying vector DB for the most similar prompt to: {user_prompt}")

    results = index.search(
        namespace="default", 
        query={"inputs": {"text": user_prompt}, "top_k": 1},
        fields=["text"]
    )

    if results['result']['hits']:
        most_similar_prompt = results['result']['hits'][0]['fields']['text']
        qid = results['result']['hits'][0]['_id']
        logging.info(f"Found most similar prompt: {most_similar_prompt} {qid}")
        return qid, most_similar_prompt
    else:
        logging.error("No similar prompt found.")
        return None, None

def retrieve_previous_prompt(qid: str) -> str:
    """
    Retrieve the previous prompt and LLM response from the datastore directory using the qid.
    Assumes files are named by qid.json and located in app/datastore.
    Returns both prompt and LLM response as a single string.
    """
    script_dir = os.path.dirname(os.path.abspath(__file__))
    datastore_directory = os.path.join(script_dir, "..", "datastore")
    datastore_directory = os.path.abspath(datastore_directory)

    file_path = os.path.join(datastore_directory, f"{qid}.json")

    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            data = json.load(file)
            prompt = data.get("in", {}).get("prompt", "")
            message = data.get("out", {}).get("message", "")

            llm_response = ""
            if "💬 LLM Response:\n" in message:
                llm_response = message.split("💬 LLM Response:\n", 1)[-1].strip().split("🖼️")[0].strip()
            else:
                logging.warning("LLM response not found in message content.")

            return f"Prompt: {prompt}\nLLM Response: {llm_response}"
    else:
        logging.error(f"File for qid {qid} not found in datastore.")
        return ""

def create_final_message(user_prompt: str) -> str:
    """
    Combine querying the vector DB, retrieving the previous prompt, and current prompt
    to create and return the final compiled message.
    """
    qid, most_similar_prompt = query_vector_db(user_prompt)

    if not qid:
        return "Error: No similar prompt found in the database."

    previous_prompt_and_llm_response = retrieve_previous_prompt(qid)

    if not previous_prompt_and_llm_response:
        return "Error: Previous prompt not found in the datastore."

    compiled_message = (
        f"{previous_prompt_and_llm_response}\n"
        f"Current Prompt: {user_prompt}"
    )
    logging.info(f"Compiled message: {compiled_message}")
    
    return compiled_message



