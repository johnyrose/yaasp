from sqlalchemy import Integer, Column, String, Float, JSON

from yaasp.common.db_connection import Base


class ArticleSummaryDB(Base):
    __tablename__ = 'article_summaries'

    id = Column(Integer, primary_key=True)
    summary = Column(String, nullable=False)
    date = Column(String, nullable=False)


class StockNewsReportDB(Base):
    __tablename__ = 'stock_news_reports'

    id = Column(Integer, primary_key=True)
    stock_symbol = Column(String, nullable=False)
    news_summary = Column(String, nullable=False)
    financial_information = Column(String, nullable=False)
    general_sentiment = Column(String, nullable=False)
    sentiment_reason = Column(String, nullable=False)

    articles_summary = Column(JSON, nullable=False)
    timestamp = Column(String, nullable=False)


class StockSymbolReportDB(Base):
    __tablename__ = 'stock_symbol_reports'

    id = Column(Integer, primary_key=True)
    stock_symbol = Column(String, nullable=False)
    news_report = Column(JSON, nullable=False)
    data = Column(JSON, nullable=False)

    stock_recommendation = Column(String, nullable=False)
    stock_recommendation_reason = Column(String, nullable=False)
    position_recommendation = Column(String, nullable=False)
    position_recommendation_reason = Column(String, nullable=False)
    confidence_level = Column(Integer, nullable=False)
    stock_score = Column(Integer, nullable=False)
    stock_score_explanation = Column(String, nullable=False)
    confidence_explanation = Column(String, nullable=False)
    timestamp = Column(String, nullable=False)


class StockRecommendationDB(Base):
    __tablename__ = 'stock_recommendations'

    id = Column(Integer, primary_key=True)
    symbol = Column(String, nullable=False)
    target_price = Column(Float, nullable=False)
    position = Column(String, nullable=False)
    amount = Column(Integer, nullable=False)
    explanation = Column(String, nullable=False)
    timestamp = Column(String, nullable=False)


class PurchaseRecommendationDB(Base):
    __tablename__ = 'purchase_recommendations'

    id = Column(Integer, primary_key=True)
    explanation = Column(String, nullable=False)
    confidence_level = Column(Integer, nullable=False)

    stock_recommendations = Column(JSON, nullable=False)
    timestamp = Column(String, nullable=False)


class CompanyStockInfoDB(Base):
    __tablename__ = 'company_stock_infos'

    id = Column(Integer, primary_key=True)
    industry = Column(String, nullable=False)
    sector = Column(String, nullable=False)
    fullTimeEmployees = Column(Integer, nullable=True)
    previousClose = Column(Float, nullable=False)
    open = Column(Float, nullable=False)
    dayLow = Column(Float, nullable=False)
    dayHigh = Column(Float, nullable=False)
    regularMarketVolume = Column(Integer, nullable=False)
    marketCap = Column(Integer, nullable=False)
    fiftyTwoWeekLow = Column(Float, nullable=False)
    fiftyTwoWeekHigh = Column(Float, nullable=False)
    twoHundredDayAverage = Column(Float, nullable=False)
    trailingAnnualDividendYield = Column(Float, nullable=True)
    sharesShort = Column(Integer, nullable=True)
    heldPercentInstitutions = Column(Float, nullable=True)
    pegRatio = Column(Float, nullable=True)
    exchange = Column(String, nullable=False)
    symbol = Column(String, nullable=False)
    underlyingSymbol = Column(String, nullable=True)
    description = Column(String, nullable=False)
    bid = Column(Float, nullable=False)
    ask = Column(Float, nullable=False)
    last = Column(Float, nullable=False)
    change = Column(Float, nullable=False)
    days_range = Column(String, nullable=False)
    fifty_two_week_range = Column(String, nullable=False)
    volume = Column(Integer, nullable=False)
    avg_volume = Column(Integer, nullable=False)
    pe_ratio = Column(Float, nullable=True)
    eps = Column(Float, nullable=True)
    earnings_date = Column(String, nullable=True)
    dividend = Column(Float, nullable=True)
    dividend_yield = Column(Float, nullable=True)
    ex_dividend_date = Column(String, nullable=True)
    company_earnings = Column(JSON, nullable=True)
    timestamp = Column(String, nullable=False)
