import os

from stock_analysis.models import OpenAIModelType

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

NEWS_API_KEY = os.getenv('NEWS_API_KEY')
MARKETAUX_API_KEY = os.getenv('MARKETAUX_API_KEY')

FINHUB_API_KEY = os.getenv('FINHUB_API_KEY')

OPENAI_MODEL_FOR_SIMPLE_TASKS = OpenAIModelType.GPT_35_TURBO
OPENAI_MODEL_FOR_COMPLICATED_TASKS = OpenAIModelType.GPT_4
