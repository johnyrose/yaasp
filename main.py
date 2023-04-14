from data_collection.company_stock_data_collector import get_stock_info
from data_collection.news_collection.marketaux_collector import MarketauxNewsCollector
from data_collection.news_collection.news_api_collector import NewsAPICollector
from stock_analysis.news_report_generator import generate_news_report

if __name__ == '__main__':
    # r = MarketauxNewsCollector('VOO')
    # print(r.get_news_articles())
    news_api_articles = NewsAPICollector('MSFT').get_news_articles()
    marketaux_articles = MarketauxNewsCollector('MSFT').get_news_articles()
    r = generate_news_report('MSFT', news_api_articles + marketaux_articles)
    print(r)