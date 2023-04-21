from typing import List

from sqlalchemy import func, desc

from common.db_connection import session_object
from common.db_utils import from_sqlalchemy
from common.models.db_objects import PurchaseRecommendationDB
from common.models.recommendations import PurchaseRecommendation


def get_all_purchase_recommendations() -> List[PurchaseRecommendation]:
    purchase_recommendations_db = session_object.query(PurchaseRecommendationDB).all()
    return [from_sqlalchemy(recommendation_db) for recommendation_db in purchase_recommendations_db]


def get_most_recent_purchase_recommendation() -> PurchaseRecommendation:
    most_recent_recommendations_subquery = (
        session_object.query(
            PurchaseRecommendationDB.stock_recommendations,
            func.max(PurchaseRecommendationDB.timestamp).label("max_timestamp"),
        )
        .group_by(PurchaseRecommendationDB.stock_recommendations)
        .subquery()
    )

    most_recent_recommendations_db = (
        session_object.query(PurchaseRecommendationDB)
        .join(
            most_recent_recommendations_subquery,
            (
                (PurchaseRecommendationDB.stock_recommendations == most_recent_recommendations_subquery.c.stock_recommendations)
                & (PurchaseRecommendationDB.timestamp == most_recent_recommendations_subquery.c.max_timestamp)
            )
        )
        .order_by(desc(PurchaseRecommendationDB.timestamp))
        .all()
    )

    return next(from_sqlalchemy(report_db) for report_db in most_recent_recommendations_db)
