import json
import os

from common.models.stock_analysis import OpenAIModelType


# Load JSON configuration
config_path = os.getenv("CONFIG_PATH", "./config.json")
with open(config_path) as config_file:
    config = json.load(config_file)

# Load sections
api_keys = config.get("api_keys", {})
news_sources_config = config.get("news_sources", ["newsapi", "marketaux"])
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

# OpenAI models
OPENAI_MODEL_FOR_SIMPLE_TASKS = OpenAIModelType[os.getenv("OPENAI_MODEL_FOR_SIMPLE_TASKS",
                                                          openai_models.get("simple_tasks", "GPT_35_TURBO"))]
OPENAI_MODEL_FOR_COMPLICATED_TASKS = OpenAIModelType[os.getenv("OPENAI_MODEL_FOR_COMPLICATED_TASKS",
                                                               openai_models.get("complicated_tasks", "GPT_4"))]

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