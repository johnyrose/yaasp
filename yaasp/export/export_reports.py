from yaasp.common.models.export_type import ExportType
from yaasp.common.models.recommendations import PurchaseRecommendation
from yaasp.common.models.stock_analysis import StockSymbolReport
from yaasp.export.export_purchase_recommendation_to_pdf import export_purchase_recommendation_to_pdf
from yaasp.export.export_reports_to_json import export_stock_symbol_report_to_json, export_purchase_recommendation_to_json
from yaasp.export.export_stock_report_to_pdf import export_stock_report_to_pdf


def export_stock_report(export_type: ExportType, stock_report: StockSymbolReport) -> str:
    if export_type == ExportType.JSON:
        return export_stock_symbol_report_to_json(stock_report)
    elif export_type == ExportType.PDF:
        return export_stock_report_to_pdf(stock_report)
    else:
        raise ValueError(f"Unsupported export type: {export_type}")


def export_purchase_recommendation(export_type: ExportType, purchase_recommendation: PurchaseRecommendation) -> str:
    if export_type == ExportType.JSON:
        return export_purchase_recommendation_to_json(purchase_recommendation)
    elif export_type == ExportType.PDF:
        return export_purchase_recommendation_to_pdf(purchase_recommendation)
    else:
        raise ValueError(f"Unsupported export type: {export_type}")