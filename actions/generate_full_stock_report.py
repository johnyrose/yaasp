import datetime
import json
from typing import List

from common.db_utils import save_to_db
from common.logger import logger
from common.openai_adapter import get_openai_response
from common.openai_prompts import GET_SEARCH_TERMS_FOR_SELF_REFLEXION
from config import OPENAI_MODEL_FOR_SIMPLE_TASKS
from common.models.data_collection import NewsArticle, CompanyStockInfo
from data_collection.news_collection.news_api_collector import NewsAPICollector
from data_collection.stock_data_collection.company_stock_data_collector import get_stock_info, \
    get_company_name_from_symbol
from common.models.stock_analysis import StockSymbolReport
from stock_analysis.news_report_generator import generate_news_report
from stock_analysis.stock_symbol_report_generator import generate_stock_symbol_report


def get_stock_news(stock_symbol: str, days_ago_news: int = 5) -> List[NewsArticle]:
    company_name = get_company_name_from_symbol(stock_symbol)
    # TODO - If the stock symbol is an index, handle it accordingly and don't lookup a company name.

    end_date = datetime.date.today()
    start_date = end_date - datetime.timedelta(days=days_ago_news)

    search_queries = [stock_symbol, company_name, f"{company_name} stock"]
    articles = []
    for query in search_queries:
        try:
            articles += NewsAPICollector(query).get_news_articles(num_articles=4, from_param=start_date)
        except Exception as e:
            logger.warning(f"Failed to get news for {query} with the following error: {e}")

    return articles


def perform_self_reflexion(current_report: StockSymbolReport, current_news_articles: List[NewsArticle],
                           days_ago_news: int, stock_info: CompanyStockInfo) -> StockSymbolReport:
    end_date = datetime.date.today()
    start_date = end_date - datetime.timedelta(days=days_ago_news)

    prompt = GET_SEARCH_TERMS_FOR_SELF_REFLEXION.format(
        confidence_level_suggestions=current_report.confidence_explanation)
    response = get_openai_response(prompt, OPENAI_MODEL_FOR_SIMPLE_TASKS)
    search_terms = json.loads(response)
    for term in search_terms:
        try:
            articles = NewsAPICollector(term).get_news_articles(num_articles=3, from_param=start_date)
            current_news_articles += articles
        except Exception as e:
            logger.warning(f"Failed to get news for {term} with the following error: {e}")
    updated_news_report = generate_news_report(current_report.stock_symbol, current_news_articles)
    new_full_report = generate_stock_symbol_report(current_report.stock_symbol, updated_news_report, stock_info)
    return new_full_report


def generate_full_stock_report(stock_symbol: str, days_ago_news: int = 5,
                               attempt_self_reflexion: bool = True) -> StockSymbolReport:
    stock_news = get_stock_news(stock_symbol, days_ago_news)
    # marketaux_articles = MarketauxNewsCollector(stock_symbol).get_news_articles(start_date=start_date)
    stock_report = generate_news_report(stock_symbol, stock_news)
    stock_info = get_stock_info(stock_symbol)
    full_report = generate_stock_symbol_report(stock_symbol, stock_report, stock_info)
    if attempt_self_reflexion:
        try:
            full_report = perform_self_reflexion(full_report, stock_news, days_ago_news, stock_info)
        except Exception as e:
            logger.warning(f"Failed to perform self reflexion with the following error: {e}")
    save_to_db(full_report)
    return full_report
