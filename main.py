from data_collection.company_stock_data_collector import get_stock_info
from data_collection.news_collection.marketaux_collector import MarketauxNewsCollector
from data_collection.news_collection.news_api_collector import NewsAPICollector


if __name__ == '__main__':
    # r = MarketauxNewsCollector('VOO')
    # print(r.get_news_articles())
    print(get_stock_info("VOO"))
