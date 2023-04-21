import concurrent.futures
from typing import List

from actions.generate_full_stock_report import generate_stock_report
from common.db_connection import session_object
from common.db_utils import from_sqlalchemy
from common.models.db_objects import StockSymbolReportDB
from common.models.stock_analysis import StockSymbolReport


def get_all_stock_symbol_reports() -> List[StockSymbolReport]:
    stock_symbol_reports_db = session_object.query(StockSymbolReportDB).all()
    return [from_sqlalchemy(report_db) for report_db in stock_symbol_reports_db]


# if __name__ == '__main__':
#     res = get_all_stock_symbol_reports()
#     print(res)
if __name__ == '__main__':

    def get_report(symbol):
        report = generate_stock_report(symbol, days_ago_news=3, attempt_self_reflexion=False)

    symbols = ["MSFT", "GOOGL", "INTC", "AMD", "EA", "ATVI", "TSLA", "AAPL", "NVDA", "BBBY"]
    symbols = ["MSFT", "GOOGL", "EA", "AMD", "TSLA", "BBBY"]
    with concurrent.futures.ThreadPoolExecutor(max_workers=6) as executor:
        futures = [executor.submit(get_report, value) for value in symbols]
        results = [future.result() for future in concurrent.futures.as_completed(futures)]
    print(results)
    # files = os.listdir('exports/stock_symbol_reports')
    # stock_reports = [StockSymbolReport(**json.load(open(f'exports/stock_symbol_reports/{f}'))) for f in files]

    # current_situation = """
    # Here is my current portfolio CSV:
    # "Symbol","Description","Quantity","MarkPrice","FifoPnlUnrealized","OpenPrice","ReportDate"
    # "AAPL","APPLE INC","1","165.56","-1.22","166.78","2023-04-13"
    # "AMD","ADVANCED MICRO DEVICES","5","92.09","-10.9","94.27","2023-04-13"
    # "BBBY","BED BATH & BEYOND INC","102","0.2565","-13.334699","0.387202941","2023-04-13"
    # "GOOGL","ALPHABET INC-CL A","3","107.43","6.11","105.393333333","2023-04-13"
    # "INTC","INTEL CORP","10","32.13","-10.85","33.215","2023-04-13"
    # "MSFT","MICROSOFT CORP","2","289.84","6.48","286.6","2023-04-13"
    # "NVDA","NVIDIA CORP","4","264.63","-36.94","273.865","2023-04-13"
    # "VOO","VANGUARD S&P 500 ETF","24","379.77","85.048","376.226333333","2023-04-13"
    #
    # I like technology and video games. I have about 4000 USD I want to invest. I want to invest for the short term to make a quick profit, not the long term. Make sure to make it diverse, I want 4-5 companies
    # """

    # stock_reports = stock_reports[:MAX_REPORTS_FOR_RECOMMENDATIONS]
    # recs = get_recommendations(stock_reports, current_situation, RiskPreference.RISKY)
    # export_purchase_recommendation_to_pdf(recs, 'recommendation.pdf')
    # print(recs.dict())

