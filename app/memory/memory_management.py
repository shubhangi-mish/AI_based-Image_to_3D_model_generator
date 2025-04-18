import os
import json
import time
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from dotenv import load_dotenv
from pinecone import Pinecone

load_dotenv()

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_HOST = os.getenv("PINECONE_HOST")
INDEX_NAME = "openfabric"
NAMESPACE = "default"
DATASTORE_PATH = "datastore"

pc = Pinecone(api_key=PINECONE_API_KEY)
index = pc.Index(INDEX_NAME, host=PINECONE_HOST)

uploaded_file_paths = set()

def fetch_existing_file_paths():
    print("Fetching records from Pinecone...")
    file_paths = set()
    next_token = None

    while True:
        response = index.list_records(
            namespace=NAMESPACE,
            include_metadata=True,
            next_token=next_token,
            limit=100
        )

        for vector in response.get("vectors", []):
            metadata = vector.get("metadata", {})
            file_path = metadata.get("file_path")
            if file_path:
                file_paths.add(file_path)

        next_token = response.get("next_token")
        if not next_token:
            break

    print(f"Fetched {len(file_paths)} records from Pinecone.")
    return file_paths

class FileSyncHandler(FileSystemEventHandler):
    EXCLUDED_FILES = {"state.json", "token.json"}

    def on_created(self, event):
        if self._is_valid_json_file(event):
            self.sync_file(event.src_path)

    def on_modified(self, event):
        if self._is_valid_json_file(event):
            self.sync_file(event.src_path)

    def _is_valid_json_file(self, event):
        return not event.is_directory and event.src_path.endswith(".json") and Path(event.src_path).name not in self.EXCLUDED_FILES

    def sync_file(self, file_path):
        if file_path in uploaded_file_paths:
            print(f"Already synced: {file_path}")
            return

        result = extract_info_from_file(file_path)
        if result:
            qid, prompt, response = result
            combined_text = format_for_embedding(prompt, response)
            upload_to_pinecone(qid, combined_text, file_path)
            uploaded_file_paths.add(file_path)

def extract_info_from_file(file_path):
    try:
        with open(file_path, "r") as f:
            data = json.load(f)
            qid = data.get("ray", {}).get("qid")
            prompt = data.get("in", {}).get("prompt")
            response = data.get("out", {}).get("message")
            return qid, prompt, response
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return None

def format_for_embedding(prompt, response):
    return f"Prompt: {prompt}\nResponse: {response}"

def upload_to_pinecone(qid, text, file_path):
    if not qid:
        print("⚠️ Skipped upload — missing QID")
        return
    try:
        index.upsert_records(
            namespace=NAMESPACE,
            records=[{
                "id": qid,
                "text": text,
                "metadata": {
                    "file_path": file_path
                }
            }]
        )
        print(f"Uploaded: {qid}")
    except Exception as e:
        print(f"Upload failed for {qid}: {e}")

def start_file_watcher():
    global uploaded_file_paths
    uploaded_file_paths = fetch_existing_file_paths()

    for file in Path(DATASTORE_PATH).glob("*.json"):
        if file.name not in FileSyncHandler.EXCLUDED_FILES and str(file) not in uploaded_file_paths:
            result = extract_info_from_file(str(file))
            if result:
                qid, prompt, response = result
                combined_text = format_for_embedding(prompt, response)
                upload_to_pinecone(qid, combined_text, str(file))
                uploaded_file_paths.add(str(file))

    observer = Observer()
    observer.schedule(FileSyncHandler(), path=DATASTORE_PATH, recursive=True)
    observer.start()
    print(f"Watching {DATASTORE_PATH}...")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

if __name__ == "__main__":
    start_file_watcher()
