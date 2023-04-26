import json
import os

from yaasp.common.logger import logger
from yaasp.common.models.stock_analysis import OpenAIModelType


# Load JSON configuration
config_path = os.getenv("CONFIG_PATH", "../config.json")

try:
    with open(config_path) as config_file:
        config = json.load(config_file)
except FileNotFoundError:
    logger.warning(f"Config file not found at {config_path}. Make sure to create it according to the documentation.")

# Load sections
api_keys = config.get("api_keys", {})
news_sources_config = config.get("news_sources", ["newsapi", "marketaux"])
models = config.get("models", {})
openai_models = config.get("openai_models", {})
reports_and_recommendations = config.get("reports_and_recommendations", {})
directories = config.get("directories", {})
database = config.get("database", {})
threading = config.get("threading", {})

# API keys
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", api_keys.get("openai_api_key"))
NEWS_API_KEY = os.getenv("NEWS_API_KEY", api_keys.get("news_api_key"))
MARKETAUX_API_KEY = os.getenv("MARKETAUX_API_KEY", api_keys.get("marketaux_api_key"))
FINNHUB_API_KEY = os.getenv("FINNHUB_API_KEY", api_keys.get("finnhub_api_key"))

# News sources
NEWS_SOURCES_TO_USE = os.getenv("NEWS_SOURCES_TO_USE", news_sources_config)

# Model configurations
GENERATING_NEWS_REPORT_MODEL = OpenAIModelType[os.getenv("GENERATING_NEWS_REPORT_MODEL",
                                                         models.get("generating_news_report_model", "GPT_4"))]
GENERATING_STOCK_SYMBOL_REPORT_MODEL = OpenAIModelType[os.getenv("GENERATING_STOCK_SYMBOL_REPORT_MODEL",
                                                                 models.get("generating_stock_symbol_report_model", "GPT_4"))]
GENERATING_PURCHASE_RECOMMENDATIONS_MODEL = \
    OpenAIModelType[os.getenv("GENERATING_PURCHASE_RECOMMENDATIONS_MODEL",
                              models.get("generating_purchase_recommendations_model", "GPT_4"))]
SUMMARIZING_ARTICLES_MODEL = OpenAIModelType[os.getenv("SUMMARIZING_ARTICLES_MODEL",
                                                       models.get("summarizing_articles_model", "GPT_35_TURBO"))]
SEARCHING_FOR_TRENDING_STOCKS_MODEL = \
    OpenAIModelType[os.getenv("SEARCHING_FOR_TRENDING_STOCKS_MODEL",
                              models.get("searching_for_trending_stocks_model", "GPT_35_TURBO"))]

# Reports and recommendations
MAX_REPORTS_FOR_RECOMMENDATIONS = int(os.getenv("MAX_REPORTS_FOR_RECOMMENDATIONS",
                                                reports_and_recommendations.get("max_reports", 12)))

# Directories
EXPORTS_DIRECTORY = os.getenv("EXPORTS_DIRECTORY", directories.get("exports_directory", "./exports"))
STOCK_SYMBOL_REPORTS_DIRECTORY = os.getenv("STOCK_SYMBOL_REPORTS_DIRECTORY",
                                           f"{EXPORTS_DIRECTORY}/stock_symbol_reports")
RECOMMENDATIONS_DIRECTORY = os.getenv("RECOMMENDATIONS_DIRECTORY", f"{EXPORTS_DIRECTORY}/recommendations")

# Database
DB_FILE = os.getenv("DB_FILE", database.get("db_file", "./sqlite.db"))
ENABLE_SQLALCHEMY_LOGGING = os.getenv("ENABLE_SQLALCHEMY_LOGGING", database.get("enable_sqlalchemy_logging", False))

# Threading
MAX_REPORT_FETCHING_THREADS = int(os.getenv("MAX_REPORT_FETCHING_THREADS",
                                            threading.get("max_report_fetching_threads", 10)))