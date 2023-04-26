import json
from typing import List

from yaasp.common.db_utils import save_to_db
from yaasp.common.logger import logger
from yaasp.common.openai_adapter import get_openai_response
from yaasp.common.openai_prompts import GET_SEARCH_TERMS_FOR_SELF_REFLEXION
from yaasp.config import GENERATING_NEWS_REPORT_MODEL
from yaasp.common.models.data_collection import NewsArticle, CompanyStockInfo
from yaasp.data_collection.news_collection.get_stock_news import get_stock_news, get_news_for_queries
from yaasp.data_collection.stock_data_collection.company_stock_data_collector import get_stock_info
from yaasp.common.models.stock_analysis import StockSymbolReport
from yaasp.stock_analysis.news_report_generator import generate_news_report
from yaasp.stock_analysis.stock_symbol_report_generator import generate_stock_symbol_report


def perform_self_reflexion(current_report: StockSymbolReport, current_news_articles: List[NewsArticle],
                           days_ago_news: int, stock_info: CompanyStockInfo) -> StockSymbolReport:
    prompt = GET_SEARCH_TERMS_FOR_SELF_REFLEXION.format(
        confidence_level_suggestions=current_report.confidence_explanation)
    response = get_openai_response(prompt, GENERATING_NEWS_REPORT_MODEL)
    search_terms = json.loads(response)
    new_articles = get_news_for_queries(search_terms, days_ago_news)
    current_news_articles.extend(new_articles)
    updated_news_report = generate_news_report(current_report.stock_symbol, current_news_articles)
    new_full_report = generate_stock_symbol_report(current_report.stock_symbol, updated_news_report, stock_info)
    return new_full_report


def generate_full_stock_report(stock_symbol: str, days_ago_news: int = 5,
                               attempt_self_reflexion: bool = False) -> StockSymbolReport:
    stock_news = get_stock_news(stock_symbol, days_ago_news)
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
