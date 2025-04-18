import time
import json
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from pinecone import Pinecone
from dotenv import load_dotenv
import os

load_dotenv()

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_HOST = os.getenv("PINECONE_HOST")

INDEX_NAME = "openfabric"
NAMESPACE = "default"
DATASTORE_PATH = "datastore"

# Initialize Pinecone
pc = Pinecone(api_key=PINECONE_API_KEY)
index = pc.Index(INDEX_NAME, host=PINECONE_HOST)

class FileSyncHandler(FileSystemEventHandler):
    EXCLUDED_FILES = {"state.json", "token.json"}

    def on_modified(self, event):
        if event.is_directory or not event.src_path.endswith(".json"):
            return

        if Path(event.src_path).name not in self.EXCLUDED_FILES:
            print(f"File modified: {event.src_path}")
            self.sync_file(event.src_path)

    def on_created(self, event):
        if event.is_directory or not event.src_path.endswith(".json"):
            return

        if Path(event.src_path).name not in self.EXCLUDED_FILES:
            print(f"New file created: {event.src_path}")
            self.sync_file(event.src_path)

    def sync_file(self, file_path):
        result = extract_info_from_file(file_path)
        if result:
            qid, prompt, response = result
            combined_text = format_for_embedding(prompt, response)
            upload_to_pinecone(qid, combined_text)

def extract_info_from_file(file_path):
    with open(file_path, "r") as f:
        try:
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

def upload_to_pinecone(qid, text):
    if not qid:
        print(f"Skipped upload — missing 'qid'")
        return
    try:
        index.upsert_records(
            namespace=NAMESPACE,
            records=[{
                "id": qid,
                "text": text
            }]
        )
    except Exception as e:
        print(f"Upload failed for {qid}: {str(e)}")

def start_file_watcher():
    event_handler = FileSyncHandler()
    observer = Observer()
    observer.schedule(event_handler, path=DATASTORE_PATH, recursive=True)
    observer.start()

    print(f"Watching {DATASTORE_PATH} for changes...")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

if __name__ == "__main__":
    start_file_watcher()
