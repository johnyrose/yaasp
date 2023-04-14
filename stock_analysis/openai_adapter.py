import openai

from common.logger import logger
from config import OPENAI_API_KEY
from stock_analysis.models import OpenAIModelType

openai.api_key = OPENAI_API_KEY


def get_openai_response(prompt: str, model_type: OpenAIModelType = OpenAIModelType.GPT_35_TURBO) -> str:
    logger.debug(f"Getting OpenAI response for prompt: {prompt}")
    completion = openai.ChatCompletion.create(
      model=model_type.value,
      messages=[
        {"role": "user", "content": prompt}
      ]
    )
    response = completion.choices[0].message.content
    logger.debug(f"OpenAI response: {response}")
    return response
