from data_collection.company_stock_data_collector import get_stock_info
from data_collection.news_collection.marketaux_collector import MarketauxNewsCollector
from data_collection.news_collection.news_api_collector import NewsAPICollector
from stock_analysis.models import StockNewsReport, GeneralSentiment
from stock_analysis.news_report_generator import generate_news_report
from stock_analysis.stock_symbol_report_generator import generate_stock_symbol_report

if __name__ == '__main__':
    news_api_articles = NewsAPICollector('MSFT').get_news_articles()
    marketaux_articles = MarketauxNewsCollector('MSFT').get_news_articles()
    report = generate_news_report('MSFT', news_api_articles + marketaux_articles)
    print(report)
    stock_info = get_stock_info('MSFT')
    full_report = generate_stock_symbol_report('MSFT', report, stock_info)
    print(full_report.dict())
