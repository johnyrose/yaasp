from typing import List

from sqlalchemy import func, desc

from common.db_connection import session_object
from common.db_utils import from_sqlalchemy
from common.models.db_objects import StockSymbolReportDB
from common.models.stock_analysis import StockSymbolReport


def get_most_recent_stock_symbol_reports() -> List[StockSymbolReport]:
    most_recent_reports_subquery = (
        session_object.query(
            StockSymbolReportDB.stock_symbol,
            func.max(StockSymbolReportDB.timestamp).label("max_timestamp"),
        )
        .group_by(StockSymbolReportDB.stock_symbol)
        .subquery()
    )

    most_recent_reports_db = (
        session_object.query(StockSymbolReportDB)
        .join(
            most_recent_reports_subquery,
            (
                (StockSymbolReportDB.stock_symbol == most_recent_reports_subquery.c.stock_symbol)
                & (StockSymbolReportDB.timestamp == most_recent_reports_subquery.c.max_timestamp)
            )
        )
        .order_by(desc(StockSymbolReportDB.timestamp))
        .all()
    )

    return [from_sqlalchemy(report_db) for report_db in most_recent_reports_db]


def get_all_stock_symbol_reports() -> List[StockSymbolReport]:
    stock_symbol_reports_db = session_object.query(StockSymbolReportDB).all()
    return [from_sqlalchemy(report_db) for report_db in stock_symbol_reports_db]
