from datetime import datetime
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, TableStyle, Table
from reportlab.lib.styles import getSampleStyleSheet
from yaasp.common.models.recommendations import PurchaseRecommendation
from yaasp.config import RECOMMENDATIONS_DIRECTORY
from yaasp.export.export_reports_to_json import create_directory_if_not_exists


def export_purchase_recommendation_to_pdf(purchase_recommendation: PurchaseRecommendation) -> str:
    create_directory_if_not_exists(RECOMMENDATIONS_DIRECTORY)
    filename = f"PurchaseRecommendation_{purchase_recommendation.timestamp.replace(' ', '-')}.pdf"
    file_path = str(Path(RECOMMENDATIONS_DIRECTORY) / filename)

    doc = SimpleDocTemplate(file_path, pagesize=letter)
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

    # Table Header
    table_header = [
        Paragraph('Symbol', styles['Heading3']),
        Paragraph('Target Price', styles['Heading3']),
        Paragraph('Position', styles['Heading3']),
        Paragraph('Amount', styles['Heading3']),
        Paragraph('Explanation', styles['Heading3'])
    ]

    # Stock Recommendations Table
    recommendations_data = [table_header]

    for recommendation in purchase_recommendation.stock_recommendations:
        recommendation_data = [
            Paragraph(recommendation.symbol, styles['BodyText']),
            Paragraph(str(recommendation.target_price), styles['BodyText']),
            Paragraph(recommendation.position, styles['BodyText']),
            Paragraph(str(recommendation.amount), styles['BodyText']),
            Paragraph(recommendation.explanation, styles['BodyText'])
        ]
        recommendations_data.append(recommendation_data)

    recommendations_table = Table(recommendations_data, colWidths=[doc.width / 5.0] * 5)
    recommendations_table.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 1), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))

    content.append(recommendations_table)
    content.append(Spacer(1, 12))

    # Confidence Level
    confidence_level = Paragraph(f"Confidence Level: {purchase_recommendation.confidence_level}/10",
                                 styles['BodyText'])
    content.append(confidence_level)

    # Build the PDF
    doc.build(content)
    return file_path
