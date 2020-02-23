
from typing import Dict, Optional

from jikanpy.exceptions import JikanException, APIException, ClientException, DeprecatedEndpoint

class JikanExtException(JikanException):
    """Base Exception for JikanExt"""

class PositionalArgumentException(JikanExtException):
    """Exception thrown when parameters are passed as positional arguments"""

    def __init__(self, message: Optional[str] = None, errors: Optional[Dict] = {}):

        if message is None:
            message = "JikanExt only accepts keyword arguments, e.g. jikanext.anime(id=1)"
        self.message = message
        self.errors = errors  # dict of error messages
        super().__init__(message)

class CacheMiss(JikanExtException):
    """For jikanpy_ext.ext.cache; If an item isn't found in cache"""
    pass
