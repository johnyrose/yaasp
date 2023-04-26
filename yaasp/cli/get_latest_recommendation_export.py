from yaasp.common.models.export_type import ExportType
from yaasp.db.get_purchase_recommendations import get_most_recent_purchase_recommendation
from yaasp.export.export_reports import export_purchase_recommendation


def get_latest_recommendation_export(export_type: str) -> str:
    recommendation = get_most_recent_purchase_recommendation()
    exported_rec = export_purchase_recommendation(ExportType(export_type.upper()), recommendation)

    return exported_rec
