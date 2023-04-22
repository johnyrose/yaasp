import os

from common.models.stock_analysis import OpenAIModelType

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

NEWS_API_KEY = os.getenv('NEWS_API_KEY')
MARKETAUX_API_KEY = os.getenv('MARKETAUX_API_KEY')

FINNHUB_API_KEY = os.getenv('FINNHUB_API_KEY')

OPENAI_MODEL_FOR_SIMPLE_TASKS = OpenAIModelType.GPT_35_TURBO
OPENAI_MODEL_FOR_COMPLICATED_TASKS = OpenAIModelType.GPT_4

MAX_REPORTS_FOR_RECOMMENDATIONS = int(os.getenv('MAX_REPORTS_FOR_RECOMMENDATIONS', 12))

EXPORTS_DIRECTORY = os.getenv('EXPORTS_DIRECTORY', './exports')
STOCK_SYMBOL_REPORTS_DIRECTORY = os.getenv('STOCK_SYMBOL_REPORTS_DIRECTORY',
                                                f'{EXPORTS_DIRECTORY}/stock_symbol_reports')
RECOMMENDATIONS_DIRECTORY = os.getenv('RECOMMENDATIONS_DIRECTORY', f'{EXPORTS_DIRECTORY}/recommendations')


DB_FILE = os.getenv('DB_FILE', './sqlite.db')
ENABLE_SQLALCHEMY_LOGGING = os.getenv('ENABLE_SQLALCHEMY_LOGGING', False)

MAX_REPORT_FETCHING_THREADS = int(os.getenv('MAX_REPORT_FETCHING_THREADS', 10))
