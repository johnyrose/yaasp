from data_collection.company_stock_data_collector import get_stock_info
from data_collection.news_collection.marketaux_collector import MarketauxNewsCollector
from data_collection.news_collection.news_api_collector import NewsAPICollector
from stock_analysis.models import StockNewsReport, GeneralSentiment
from stock_analysis.news_report_generator import generate_news_report

if __name__ == '__main__':
    # r = MarketauxNewsCollector('VOO')
    # print(r.get_news_articles())
    # news_api_articles = NewsAPICollector('MSFT').get_news_articles()
    # marketaux_articles = MarketauxNewsCollector('MSFT').get_news_articles()
    # r = generate_news_report('MSFT', news_api_articles + marketaux_articles)
    report = StockNewsReport(
        stock_symbol='MSFT',
        news_summary="Cathie Wood, the founder and CEO of ARK Invest, has added Microsoft (MSFT) stocks to her ARK Next Generation Internet ETF (ARKW), showcasing her confidence in the company's future growth in areas such as cloud computing and AI. MSFT also made the list of top 10 dividend growth stocks for April 2023, highlighting its strong market position and continuous innovation. However, potential regulation on AI tools like ChatGPT, in which Microsoft holds an exclusive multi-billion-dollar license, may have implications for the company, though it signals a growing awareness of AI's potential risks.",
        financial_information="Microsoft's share price increased by 35% in the last year, outperforming the S&P 500 and showing strong potential in the HDR and AI markets.",
        general_sentiment=GeneralSentiment.POSITIVE,
        sentiment_reason="Cathie Wood's purchase of MSFT stock and its inclusion in the top 10 dividend growth stocks point towards a positive outlook."
    )
    stock_info = get_stock_info('MSFT')
    print(report)