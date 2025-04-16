import logging
from typing import Any, Dict, List, Literal, Tuple

import requests

from core.remote import Remote

# Type aliases for clarity
Manifests = Dict[str, dict]
Schemas = Dict[str, Tuple[dict, dict]]
Connections = Dict[str, Remote]


class Stub:
    """
    Stub acts as a lightweight client interface that initializes remote connections
    to multiple Openfabric applications, fetching their manifests, schemas, and enabling
    execution of calls to these apps.

    Attributes:
        _schema (Schemas): Stores input/output schemas for each app ID.
        _manifest (Manifests): Stores manifest metadata for each app ID.
        _connections (Connections): Stores active Remote connections for each app ID.
    """

    # ----------------------------------------------------------------------
    def __init__(self, app_ids: List[str]):
        """
        Initializes the Stub instance by loading manifests, schemas, and connections
        for each given app ID.

        Args:
            app_ids (List[str]): A list of application identifiers (hostnames or URLs).
        """
        self._schema: Schemas = {}
        self._manifest: Manifests = {}
        self._connections: Connections = {}

        for app_id in app_ids:
            base_url = app_id.strip('/')

            try:
                # Fetch manifest
                manifest = requests.get(f"https://{base_url}/manifest").json()
                logging.info(f"[{app_id}] Manifest loaded.")
                self._manifest[app_id] = manifest

                # Fetch input schema
                input_schema = requests.get(f"https://{base_url}/schema?type=input").json()
                logging.info(f"[{app_id}] Input schema loaded.")

                # Fetch output schema
                output_schema = requests.get(f"https://{base_url}/schema?type=output").json()
                logging.info(f"[{app_id}] Output schema loaded.")
                self._schema[app_id] = (input_schema, output_schema)

                # Establish Remote WebSocket connection
                self._connections[app_id] = Remote(f"wss://{base_url}", f"{app_id}-proxy").connect()
                logging.info(f"[{app_id}] Connection established.")
            except Exception as e:
                logging.error(f"[{app_id}] Initialization failed: {e}")

    # ----------------------------------------------------------------------
    def call(self, app_id: str, data: Any, uid: str = 'super-user') -> dict:
        """
        Sends a request to the specified app via its Remote connection.

        Args:
            app_id (str): The application ID to route the request to.
            data (Any): The input data to send to the app.
            uid (str): The unique user/session identifier for tracking (default: 'super-user').

        Returns:
            dict: The output data returned by the app.

        Raises:
            Exception: If no connection is found for the provided app ID, or execution fails.
        """
        connection = self._connections.get(app_id)
        if not connection:
            raise Exception(f"Connection not found for app ID: {app_id}")

        try:
            handler = connection.execute(data, uid)
            result = connection.get_response(handler)
            logging.info(f"[{app_id}] Output: {result}")
            return result
        except Exception as e:
            logging.error(f"[{app_id}] Execution failed: {e}")
            raise

    # ----------------------------------------------------------------------
    def manifest(self, app_id: str) -> dict:
        """
        Retrieves the manifest metadata for a specific application.

        Args:
            app_id (str): The application ID for which to retrieve the manifest.

        Returns:
            dict: The manifest data for the app, or an empty dictionary if not found.
        """
        return self._manifest.get(app_id, {})

    # ----------------------------------------------------------------------
    def schema(self, app_id: str, type: Literal['input', 'output']) -> dict:
        """
        Retrieves the input or output schema for a specific application.

        Args:
            app_id (str): The application ID for which to retrieve the schema.
            type (Literal['input', 'output']): The type of schema to retrieve.

        Returns:
            dict: The requested schema (input or output).

        Raises:
            ValueError: If the schema type is invalid or the schema is not found.
        """
        _input, _output = self._schema.get(app_id, (None, None))

        if type == 'input':
            if _input is None:
                raise ValueError(f"Input schema not found for app ID: {app_id}")
            return _input
        elif type == 'output':
            if _output is None:
                raise ValueError(f"Output schema not found for app ID: {app_id}")
            return _output
        else:
            raise ValueError("Type must be either 'input' or 'output'")
