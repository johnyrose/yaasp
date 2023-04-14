import json
from typing import List

from data_collection.models import NewsArticle
from openai_prompts import GET_ARTICLE_SUMMARY_PROMPT, GET_ARTICLE_NEWS_REPORT
from stock_analysis.models import OpenAIModelType, StockNewsReport
from stock_analysis.openai_adapter import get_openai_response


def get_articles_summaries(company_symbol: str, news_articles: List[NewsArticle]) -> List[str]:
    article_summaries = []
    for article in news_articles:
        print(f'Getting summary for article: {article.title}...')
        summary = get_openai_response(
            prompt=GET_ARTICLE_SUMMARY_PROMPT.format(company_name=company_symbol, title=article.title,
                                                     content=article.body),
            model_type=OpenAIModelType.GPT_4)
        article_summaries.append(summary)
    return article_summaries


def _get_news_report(stock_symbol: str, article_summaries: List[str]) -> StockNewsReport:
    print(f'Getting news report for {stock_symbol}...')
    prompt = GET_ARTICLE_NEWS_REPORT.format(stock_symbol=stock_symbol, article_summaries=article_summaries)
    retry_count = 4  # TODO - Make this configurable
    for i in range(retry_count):
        try:
            openai_response = get_openai_response(prompt=prompt, model_type=OpenAIModelType.GPT_4)
            response_json = json.loads(openai_response)
            return StockNewsReport(**response_json)
        except Exception as e:
            if i == retry_count - 1:
                raise e
            print('Failed to get news report from OpenAI, retrying...')


def generate_news_report(stock_symbol: str, news_articles: List[NewsArticle]) -> StockNewsReport:
    article_summaries = get_articles_summaries(stock_symbol, news_articles)
    news_report = _get_news_report(stock_symbol, article_summaries)
    return news_report
