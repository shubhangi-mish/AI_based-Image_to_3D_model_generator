import logging
from typing import Dict

from ontology_dc8f06af066e4a7880a5938933236037.config import ConfigClass
from ontology_dc8f06af066e4a7880a5938933236037.input import InputClass
from ontology_dc8f06af066e4a7880a5938933236037.output import OutputClass
from openfabric_pysdk.context import State
from core.local_llm import run_local_llm  # Importing the local LLM handler
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

    # Get LLM response by calling the run_local_llm function from core.llm_handler
    prompt = request.prompt
    llm_response = run_local_llm(prompt)

    # Prepare the response as a dictionary
    response_dict = {
        "message": llm_response
    }

    # Return the dictionary instead of OutputClass
    return response_dict


