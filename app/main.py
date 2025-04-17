import logging
from typing import Dict

from ontology_dc8f06af066e4a7880a5938933236037.config import ConfigClass
from ontology_dc8f06af066e4a7880a5938933236037.input import InputClass
from ontology_dc8f06af066e4a7880a5938933236037.output import OutputClass
from openfabric_pysdk.context import State
from core.local_llm import run_local_llm
from core.txt_to_img import run_text_to_image 
from core.img_to_3d import run_image_to_3d
from core.stub import Stub

# ----------------------------------------------------------
# Global configuration dictionary
# ----------------------------------------------------------
configurations: Dict[str, ConfigClass] = dict()

# ----------------------------------------------------------
# Config callback function
# ----------------------------------------------------------
def config(configuration: Dict[str, ConfigClass], state: State) -> None:
    for uid, conf in configuration.items():
        logging.info(f"Saving new config for user: '{uid}'")
        configurations[uid] = conf

# ----------------------------------------------------------
# Execute callback function (the one Execution API calls)
# ----------------------------------------------------------
def execute(request: InputClass, response: OutputClass, state: State) -> Dict[str, str]:
    logging.info(f"Received prompt: {request.prompt}")
  
    user_config: ConfigClass = configurations.get('super-user', None)
    app_ids = user_config.app_ids if user_config else []
    stub = Stub(app_ids)

    # Getting LLM response
    prompt = request.prompt
    llm_response = run_local_llm(prompt)

    # Getting the Text-to-Image result
    text2image_response = run_text_to_image(llm_response, app_ids)
    print(text2image_response)

    image_blob_reference = text2image_response.get("result", "")  

    if image_blob_reference:
        # Getting result from image to 3D app
        image_to_3d_response = run_image_to_3d(image_blob_reference, app_ids)
    else:
        image_to_3d_response = {"message": "Image blob reference not found in Text-to-Image response."}

    full_message = (
        f"🧠 Prompt: {prompt}\n\n"
        f"💬 LLM Response:\n{llm_response}\n\n"
        f"🖼️ Text-to-Image Result:\n{image_blob_reference}\n\n" 
        f"🔲 Image-to-3D Result:\n{image_to_3d_response['message']}"
    )

    return {
        "message": full_message
    }
