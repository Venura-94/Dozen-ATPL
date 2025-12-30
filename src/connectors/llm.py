import os

from openai import OpenAI


class LLM:

    __client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

    @classmethod
    def get_openai_client(cls) -> OpenAI:
        return cls.__client