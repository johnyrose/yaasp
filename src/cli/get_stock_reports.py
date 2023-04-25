from typing import List

from src.common.models.export_type import ExportType
from src.db.get_stock_symbol_reports import get_most_recent_stock_symbol_reports, get_all_stock_symbol_reports
from src.export.export_reports import export_stock_report


def get_current_stock_reports(latest: bool, export_type: str) -> List[str]:
    if latest:
        reports = get_most_recent_stock_symbol_reports()
    else:
        reports = get_all_stock_symbol_reports()

    exported_files = [export_stock_report(ExportType(export_type.upper()), report) for report in reports]

    return exported_files
