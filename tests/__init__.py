"""Provide tests."""
from pathlib import Path

from pydantic import BaseModel  # pylint: disable=no-name-in-module

ROOT_PATH = Path(__file__).parent.parent
TEST_CONTENT = "test content"
ZIP_FILE = "foo.zip"
ZIP_FILE_ASCII_CONTENT = (
    "UEsDBBQACAAIAEZnbVAAAAAAAAAAAAwAAAAHACAAZm9vLnR4dFVUDQAHVXVrXlV1a17JfWtedXgLAAE"
    "E6AMAAAToAwAAS8vP50pKLALiKi4AUEsHCBsKPpQMAAAADAAAAFBLAQIUAxQACAAIAEZnbVAbCj6UDA"
    "AAAAwAAAAHACAAAAAAAAAAAACkgQAAAABmb28udHh0VVQNAAdVdWteVXVrXsl9a151eAsAAQToAwAAB"
    "OgDAABQSwUGAAAAAAEAAQBVAAAAYQAAAAAA"
)


class RequestParams(BaseModel):
    """Represent parameters of a client request."""

    params: dict
