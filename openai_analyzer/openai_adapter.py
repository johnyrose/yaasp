import openai

from config import OPENAI_API_KEY
from openai_analyzer.models import OpenAIModelType


openai.api_key = OPENAI_API_KEY


def get_openai_response(prompt: str, model_type: OpenAIModelType = OpenAIModelType.GPT_35_TURBO) -> str:
    completion = openai.ChatCompletion.create(
      model=model_type.value,
      messages=[
        {"role": "user", "content": prompt}
      ]
    )
    response = completion.choices[0].message.content
    return response
