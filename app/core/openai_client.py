import os

from openai import OpenAI


def get_openai_client() -> OpenAI:
    return OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
