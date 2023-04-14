from data_collection.news_collection.news_api_collector import NewsAPICollector


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    r = NewsAPICollector('tesla')
    print(r.get_news_articles())
