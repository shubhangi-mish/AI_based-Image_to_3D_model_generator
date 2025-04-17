from openfabric_pysdk.starter import Starter
import threading
import subprocess
import time

def run_backend():
    PORT = 8888
    Starter.ignite(debug=False, host="0.0.0.0", port=PORT)

def run_frontend():
    # Wait a moment to ensure backend is ready
    time.sleep(3)
    subprocess.run(["streamlit", "run", "ui.py", "--server.port=8501"])

if __name__ == '__main__':
    backend_thread = threading.Thread(target=run_backend)
    frontend_thread = threading.Thread(target=run_frontend)

    backend_thread.start()
    frontend_thread.start()

    backend_thread.join()
    frontend_thread.join()
