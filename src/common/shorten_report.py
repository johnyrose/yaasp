from typing import Dict

from src.common.models.stock_analysis import StockSymbolReport


def get_shortened_stock_symbol_report(report: StockSymbolReport) -> Dict:
    report_json = report.dict()
    data = report_json.get("data", {})
    news_report = report_json.get("news_report", {})
    company_earnings = data.get("company_earnings", [])

    condensed_json = {
        "stock_symbol": report_json.get("stock_symbol"),
        "industry": data.get("industry"),
        "sector": data.get("sector"),
        "previousClose": data.get("previousClose"),
        "dayLow": data.get("dayLow"),
        "dayHigh": data.get("dayHigh"),
        "marketCap": data.get("marketCap"),
        "fiftyTwoWeekLow": data.get("fiftyTwoWeekLow"),
        "fiftyTwoWeekHigh": data.get("fiftyTwoWeekHigh"),
        "pe_ratio": data.get("pe_ratio"),
        "eps": data.get("eps"),
        "dividend_yield": data.get("dividend_yield"),
        "news_summary": news_report.get("news_summary"),
        "general_sentiment": news_report.get("general_sentiment"),
        "sentiment_reason": news_report.get("sentiment_reason"),
        "recent_earnings_surprises": [
            {
                "quarter": report.get("quarter"),
                "year": report.get("year"),
                "surprisePercent": report.get("surprisePercent")
            }
            for report in company_earnings
        ],
        "stock_recommendation": report_json.get("stock_recommendation"),
        "stock_recommendation_reason": report_json.get("stock_recommendation_reason"),
        "position_recommendation": report_json.get("position_recommendation"),
        "position_recommendation_reason": report_json.get("position_recommendation_reason"),
        "confidence_level": report_json.get("confidence_level"),
        "confidence_explanation": report_json.get("confidence_explanation")
    }
    return condensed_json
