"""A file containing a list of Custom Errors"""

class BadStatusException(Exception):
    """Exception raised when raise for status fails."""
    def __init__(self, err) -> None:
        super().__init__(f"An error occurred with the server: {err}")

class FailedApiRequestException(Exception):
    """Exception raised when the API returns a failed response.
    
    Arguments:
    A stringified dictionary containing:
    ERROR: The Error that occurred
    MESSAGE: The Error Message
    EXTRA: Any extra data. This may be left as an empty list"""

    def __init__(self, data_dict:str) -> None:
        super().__init__(data_dict)