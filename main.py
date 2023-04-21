import concurrent.futures
from typing import List

from sqlalchemy import desc, func

from actions.generate_full_stock_report import generate_stock_report
from actions.search_trending_stocks import search_trending_stocks
from common.db_connection import session_object
from common.db_utils import from_sqlalchemy
from common.models.db_objects import StockSymbolReportDB, PurchaseRecommendationDB
from common.models.recommendations import RiskPreference, PurchaseRecommendation
from common.models.stock_analysis import StockSymbolReport
from config import MAX_REPORTS_FOR_RECOMMENDATIONS
from db.get_purchase_recommendations import get_most_recent_purchase_recommendation, get_all_purchase_recommendations
from db.get_stock_symbol_reports import get_most_recent_stock_symbol_reports
from export.export_purchase_recommendation_to_pdf import export_purchase_recommendation_to_pdf
from recommendations_generator.get_recommendations import get_recommendations


def get_all_stock_symbol_reports() -> List[StockSymbolReport]:
    stock_symbol_reports_db = session_object.query(StockSymbolReportDB).all()
    return [from_sqlalchemy(report_db) for report_db in stock_symbol_reports_db]


# if __name__ == '__main__':
#     res = get_all_purchase_recommendations()
#     print(res)
if __name__ == '__main__':
    # symbols = search_trending_stocks()
    # print(symbols)
    #
    # def get_report(symbol):
    #     report = generate_stock_report(symbol, days_ago_news=3, attempt_self_reflexion=False)
    #
    # symbols += ["MSFT", "GOOGL", "INTC", "AMD", "EA", "ATVI", "TSLA", "AAPL", "NVDA", "BBBY"]
    # # symbols = ["MSFT", "GOOGL", "EA", "AMD", "TSLA", "BBBY"]
    # with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
    #     futures = [executor.submit(get_report, value) for value in symbols]
    #     results = [future.result() for future in concurrent.futures.as_completed(futures)]

#     # print(results)
#     # files = os.listdir('exports/stock_symbol_reports')
    stock_reports = get_most_recent_stock_symbol_reports()

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

