from datetime import datetime

from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, ListFlowable, ListItem
from reportlab.lib.styles import getSampleStyleSheet
from common.models.recommendations import PurchaseRecommendation


def export_purchase_recommendation_to_pdf(purchase_recommendation: PurchaseRecommendation, output_filename: str):
    doc = SimpleDocTemplate(output_filename, pagesize=letter)
    styles = getSampleStyleSheet()
    content = []

    # Report Header
    current_date_time = datetime.now().strftime("%Y-%m-%d %H:%M")
    report_header = Paragraph(f"Purchase Recommendations Report ({current_date_time})", styles['Heading1'])
    content.append(report_header)
    content.append(Spacer(1, 12))

    # Explanation
    explanation = Paragraph(purchase_recommendation.explanation, styles['BodyText'])
    content.append(explanation)
    content.append(Spacer(1, 12))

    # Stock Recommendations List
    recommendations_list = ListFlowable(
        [
            ListItem(
                Paragraph(
                    f"{recommendation.symbol}: Target Price {recommendation.target_price}, "
                    f"Position {recommendation.position}, Amount {recommendation.amount} - "
                    f"{recommendation.explanation}",
                    styles['BodyText']
                ),
                leftIndent=18,
            )
            for recommendation in purchase_recommendation.stock_recommendations
        ],
        bulletType='bullet',
        start='circle',
    )

    content.append(recommendations_list)
    content.append(Spacer(1, 12))

    # Confidence Level
    confidence_level = Paragraph(f"Confidence Level: {purchase_recommendation.confidence_level}/10",
                                 styles['BodyText'])
    content.append(confidence_level)

    # Build the PDF
    doc.build(content)