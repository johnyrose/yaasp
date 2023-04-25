from datetime import datetime, timedelta
from typing import Optional

from src.cli.typer_objects import console
from src.common.models.export_type import ExportType
from src.common.models.recommendations import RiskPreference
from config import MAX_REPORTS_FOR_RECOMMENDATIONS
from src.db.get_stock_symbol_reports import get_most_recent_stock_symbol_reports
from src.export.export_reports import export_purchase_recommendation
from src.recommendations_generator.generate_recommendation import generate_purchase_recommendation


def generate_recommendation_for_file(input_file: str, risk_preference: str, export_type: str,
                                     days_ago_reports: int) -> Optional[str]:
    try:
        current_situation = open(input_file, "r").read()
    except Exception as e:
        console.print(f"Error reading file: {input_file}, error: {e}")
        return

    stock_reports = get_most_recent_stock_symbol_reports()
    stock_reports_by_score = sorted(stock_reports, key=lambda x: x.stock_score, reverse=True)

    valid_timeframe = datetime.now() - timedelta(days=days_ago_reports)
    recent_stock_reports = [report for report in stock_reports_by_score if
                            datetime.strptime(report.timestamp, "%Y-%m-%d %H:%M:%S") >= valid_timeframe]

    reports_after_filtering = recent_stock_reports[:MAX_REPORTS_FOR_RECOMMENDATIONS]

    recs = generate_purchase_recommendation(reports_after_filtering,
                                            current_situation, RiskPreference(risk_preference.upper()))
    file_name = export_purchase_recommendation(ExportType(export_type.upper()), recs)

    return file_name
