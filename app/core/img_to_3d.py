from core.stub import Stub
import logging
from typing import Dict

def run_image_to_3d(image_blob_reference: str, app_ids: list) -> Dict[str, str]:
    """
    Uses Stub to call the Image-to-3D Openfabric app and get the response.

    Args:
        image_blob_reference (str): The reference to the image blob (resource path).
        app_ids (list): A list of app URLs or IDs.

    Returns:
        Dict[str, str]: A dictionary with the generated message or error.
    """
    try:
        stub = Stub(app_ids)
        
        if not app_ids:
            return {"message": "No app IDs provided."}

        app_id = app_ids[1]  
        
        data = {
            "input_image": image_blob_reference  
        }

        result = stub.call(app_id, data)
        
        if 'generated_object' in result:
            return {"message": result['generated_object']}
        elif 'video_object' in result:
            return {"message": result['video_object']}
        else:
            return {"message": "No result found in the response."}

    except Exception as e:
        logging.error(f"Image-to-3D transformation failed: {e}")
        return {"message": f"Image-to-3D failed: {str(e)}"}
