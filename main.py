import datetime
import json
import os
from actions.generate_full_stock_report import generate_stock_report
from common.shorten_report import get_shortened_stock_symbol_report
from config import MAX_REPORTS_FOR_RECOMMENDATIONS
from data_collection.news_collection.marketaux_collector import MarketauxNewsCollector
from data_collection.news_collection.news_api_collector import NewsAPICollector
from data_collection.stock_data_collection.company_stock_data_collector import get_stock_info
from export.export_purchase_recommendation_to_pdf import export_purchase_recommendation_to_pdf
from export.export_stock_report_to_pdf import export_stock_report_to_pdf
from recommendations_generator.get_recommendations import get_recommendations
from recommendations_generator.models import RiskPreference
from stock_analysis.models import StockSymbolReport


# if __name__ == '__main__':
#     get_stock_info('MSFT')

if __name__ == '__main__':
    symbols = ["MSFT", "GOOGL", "INTC", "AMD", "EA", "ATVI", "TSLA", "AAPL", "UPS", "KOL", "NVDA", "ABR", "PTPI", "PARA"]
    # stock_reports = []
    # for symbol in symbols:
    #     try:
    #         report = generate_stock_report(symbol, days_ago_news=3)
    #         stock_reports.append(report)
    #     except Exception as e:
    #         print(f'Failed to generate report for {symbol} with error: {e}')
    files = os.listdir('exports/stock_symbol_reports')
    stock_reports = [StockSymbolReport(**json.load(open(f'exports/stock_symbol_reports/{f}'))) for f in files]

    current_situation = """
    Here is my current portfolio CSV:
    "Symbol","Description","Quantity","MarkPrice","FifoPnlUnrealized","OpenPrice","ReportDate"
    "AAPL","APPLE INC","1","165.56","-1.22","166.78","2023-04-13"
    "AMD","ADVANCED MICRO DEVICES","5","92.09","-10.9","94.27","2023-04-13"
    "BBBY","BED BATH & BEYOND INC","102","0.2565","-13.334699","0.387202941","2023-04-13"
    "GOOGL","ALPHABET INC-CL A","3","107.43","6.11","105.393333333","2023-04-13"
    "INTC","INTEL CORP","10","32.13","-10.85","33.215","2023-04-13"
    "MSFT","MICROSOFT CORP","2","289.84","6.48","286.6","2023-04-13"
    "NVDA","NVIDIA CORP","4","264.63","-36.94","273.865","2023-04-13"
    "VOO","VANGUARD S&P 500 ETF","24","379.77","85.048","376.226333333","2023-04-13"

    I like technology and video games. I have about 4000 USD I want to invest. I want to invest for the short term to make a quick profit, not the long term. Make sure to make it diverse, I want 4-5 companies
    """

    stock_reports = stock_reports[:MAX_REPORTS_FOR_RECOMMENDATIONS]
    recs = get_recommendations(stock_reports, current_situation, RiskPreference.RISKY)
    export_purchase_recommendation_to_pdf(recs, 'recommendation.pdf')
    print(recs.dict())

