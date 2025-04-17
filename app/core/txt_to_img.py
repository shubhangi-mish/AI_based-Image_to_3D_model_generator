from core.stub import Stub
import logging
from typing import Dict

def run_text_to_image(prompt: str, app_ids: list) -> Dict[str, str]:
    """
    Uses Stub to call a text-to-image Openfabric app and get the response.

    Args:
        prompt (str): The input prompt to generate an image from.
        app_ids (list): A list of app URLs or IDs.

    Returns:
        Dict[str, str]: A dictionary with the generated message or error.
    """
    try:
        stub = Stub(app_ids)
        if not app_ids:
            return {"message": "No app IDs provided."}

        app_id = app_ids[0]  
        data = {
            "prompt": prompt,
            "attachments": []
        }

        result = stub.call(app_id, data)
      
        if 'result' in result:
            return {"result": result['result']} 
        else:
            return {"message": "No result found in the response."}

    except Exception as e:
        logging.error(f"Text-to-Image generation failed: {e}")
        return {"message": f"Text-to-Image failed: {str(e)}"}

