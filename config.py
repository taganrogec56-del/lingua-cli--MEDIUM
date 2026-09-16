import os
import pathlib
from dotenv import load_dotenv

ENV_FILE_NAME = '.env'
ENV_PATH = pathlib.Path(__file__).resolve().parent / ENV_FILE_NAME

REQUEST_TIMEOUT = 40

load_dotenv(ENV_PATH)


def get_translator_api_key() -> str | None:
    api_key = os.getenv('TRANSLATOR_API_KEY')
    if api_key is None:
        return None
    api_key = api_key.strip()
    return api_key or None
