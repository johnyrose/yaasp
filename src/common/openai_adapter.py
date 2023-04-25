import openai

from src.common.logger import logger
from config import OPENAI_API_KEY
from src.common.models.stock_analysis import OpenAIModelType

openai.api_key = OPENAI_API_KEY


def get_openai_response(prompt: str, model_type: OpenAIModelType = OpenAIModelType.GPT_35_TURBO) -> str:
    logger.debug(f"Getting OpenAI response for prompt: {prompt}")
    retry_count = 4  # TODO - Make this configurable
    for i in range(retry_count):
        try:
            completion = openai.ChatCompletion.create(
              model=model_type.value,
              messages=[
                {"role": "user", "content": prompt}
              ]
            )
            response = completion.choices[0].message.content
            logger.debug(f"OpenAI response: {response}")
            return response
        except Exception as e:
            if i == retry_count - 1:
                raise e
            logger.warning(f"Failed to get response from OpenAI the following error was received: {e}, retrying...")
    raise Exception("Failed to get response from OpenAI. Check the logs below more information.")
