from datetime import datetime

from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet

from common.models.stock_analysis import StockSymbolReport


def export_stock_report_to_pdf(stock_report: StockSymbolReport, output_filename: str):
    doc = SimpleDocTemplate(output_filename, pagesize=letter)
    styles = getSampleStyleSheet()
    content = []

    # Stock Symbol Header
    current_date_time = datetime.now().strftime("%Y-%m-%d %H:%M")
    stock_symbol_header = Paragraph(f"Stock Report for {stock_report.stock_symbol} ({current_date_time})",
                                    styles['Heading1'])
    content.append(stock_symbol_header)
    content.append(Spacer(1, 12))

    # Stock Recommendation
    stock_recommendation = Paragraph(
        f"Stock Recommendation: <strong>{stock_report.stock_recommendation}</strong> - {stock_report.stock_recommendation_reason}",
        styles['BodyText'])
    content.append(stock_recommendation)
    content.append(Spacer(1, 12))

    # Position Recommendation
    position_recommendation = Paragraph(
        f"Position Recommendation: <strong>{stock_report.position_recommendation}</strong> - {stock_report.position_recommendation_reason}",
        styles['BodyText'])
    content.append(position_recommendation)
    content.append(Spacer(1, 12))

    # Confidence Level
    confidence_level = Paragraph(
        f"Confidence Level: <strong>{stock_report.confidence_level}/10</strong> - {stock_report.confidence_explanation}",
        styles['BodyText'])
    content.append(confidence_level)
    content.append(Spacer(1, 12))

    # Stock Data
    stock_data_header = Paragraph("Stock Data:", styles['Heading2'])
    content.append(stock_data_header)
    content.append(Spacer(1, 12))

    stock_data_table = Table([
        ['Previous Close', stock_report.data.previousClose],
        ['Open', stock_report.data.open],
        ['Day Low', stock_report.data.dayLow],
        ['Day High', stock_report.data.dayHigh],
        ['Market Cap', stock_report.data.marketCap],
        ['52-Week Low', stock_report.data.fiftyTwoWeekLow],
        ['52-Week High', stock_report.data.fiftyTwoWeekHigh],
        # ... (add more stock data fields here) ...
    ])

    stock_data_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 14),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))

    content.append(stock_data_table)
    content.append(Spacer(1, 12))

    # News Report
    news_report_header = Paragraph("News Report:", styles['Heading2'])
    content.append(news_report_header)
    content.append(Spacer(1, 12))

    news_summary = Paragraph(stock_report.news_report.news_summary, styles['BodyText'])
    content.append(news_summary)
    content.append(Spacer(1, 12))

    articles_summary_header = Paragraph("Articles Summary:", styles['Heading3'])
    content.append(articles_summary_header)
    content.append(Spacer(1, 12))

    for article in stock_report.news_report.articles_summary:
        article_paragraph = Paragraph(f"{article.date}: {article.summary}", styles['BodyText'])
    content.append(article_paragraph)
    content.append(Spacer(1, 12))

    # Build the PDF
    doc.build(content)


