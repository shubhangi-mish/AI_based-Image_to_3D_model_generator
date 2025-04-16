from typing import Optional, Union

from openfabric_pysdk.helper import Proxy
from openfabric_pysdk.helper.proxy import ExecutionResult


class Remote:
    """
    Remote is a helper class that interfaces with an Openfabric Proxy instance
    to send input data, execute computations, and fetch results synchronously
    or asynchronously.

    Attributes:
        proxy_url (str): The URL to the proxy service.
        proxy_tag (Optional[str]): An optional tag to identify a specific proxy instance.
        client (Optional[Proxy]): The initialized proxy client instance.
    """

    # ----------------------------------------------------------------------
    def __init__(self, proxy_url: str, proxy_tag: Optional[str] = None):
        """
        Initializes the Remote instance with the proxy URL and optional tag.

        Args:
            proxy_url (str): The base URL of the proxy.
            proxy_tag (Optional[str]): An optional tag for the proxy instance.
        """
        self.proxy_url = proxy_url
        self.proxy_tag = proxy_tag
        self.client: Optional[Proxy] = None

    # ----------------------------------------------------------------------
    def connect(self) -> 'Remote':
        """
        Establishes a connection with the proxy by instantiating the Proxy client.

        Returns:
            Remote: The current instance for chaining.
        """
        self.client = Proxy(self.proxy_url, self.proxy_tag, ssl_verify=False)
        return self

    # ----------------------------------------------------------------------
    def execute(self, inputs: dict, uid: str) -> Union[ExecutionResult, None]:
        """
        Executes an asynchronous request using the proxy client.

        Args:
            inputs (dict): The input payload to send to the proxy.
            uid (str): A unique identifier for the request.

        Returns:
            Union[ExecutionResult, None]: The result of the execution, or None if not connected.
        """
        if self.client is None:
            return None

        return self.client.request(inputs, uid)

    # ----------------------------------------------------------------------
    @staticmethod
    def get_response(output: ExecutionResult) -> Union[dict, None]:
        """
        Waits for the result and processes the output.

        Args:
            output (ExecutionResult): The result returned from a proxy request.

        Returns:
            Union[dict, None]: The response data if successful, None otherwise.

        Raises:
            Exception: If the request failed or was cancelled.
        """
        if output is None:
            return None

        output.wait()
        status = str(output.status()).lower()
        if status == "completed":
            return output.data()
        if status in ("cancelled", "failed"):
            raise Exception("The request to the proxy app failed or was cancelled!")
        return None

    # ----------------------------------------------------------------------
    def execute_sync(self, inputs: dict, configs: dict, uid: str) -> Union[dict, None]:
        """
        Executes a synchronous request with configuration parameters.

        Args:
            inputs (dict): The input payload.
            configs (dict): Additional configuration parameters.
            uid (str): A unique identifier for the request.

        Returns:
            Union[dict, None]: The processed response, or None if not connected.
        """
        if self.client is None:
            return None

        output = self.client.execute(inputs, configs, uid)
        return Remote.get_response(output)
