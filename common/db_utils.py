from pydantic import BaseModel

from common.db_connection import Base, session_object, db_engine
from common.models.data_collection import CompanyStockInfo
from common.models.db_objects import StockSymbolReportDB, StockNewsReportDB, ArticleSummaryDB, StockRecommendationDB, \
    PurchaseRecommendationDB, CompanyStockInfoDB
from common.models.recommendations import PurchaseRecommendation, StockRecommendation
from common.models.stock_analysis import StockSymbolReport, StockNewsReport, ArticleSummary

model_mapping = {
    ArticleSummary: ArticleSummaryDB,
    StockNewsReport: StockNewsReportDB,
    StockSymbolReport: StockSymbolReportDB,
    StockRecommendation: StockRecommendationDB,
    PurchaseRecommendation: PurchaseRecommendationDB,
    CompanyStockInfo: CompanyStockInfoDB
}


# Conversion functions
def to_sqlalchemy(obj: BaseModel) -> Base:
    sqlalchemy_model = model_mapping[obj.__class__]
    return sqlalchemy_model(**obj.dict())


def from_sqlalchemy(obj: Base) -> BaseModel:
    pydantic_model = {v: k for k, v in model_mapping.items()}[obj.__class__]
    return pydantic_model(**obj.__dict__)


def save_to_db(obj: BaseModel) -> None:
    sqlalchemy_obj = to_sqlalchemy(obj)
    Base.metadata.create_all(db_engine)
    try:
        session_object.add(sqlalchemy_obj)
        session_object.commit()
    except Exception as e:
        session_object.rollback()
        raise e
