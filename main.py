import concurrent.futures
from datetime import datetime, timedelta
from typing import List, Optional

import typer
from rich.console import Console

from actions.generate_full_stock_report import generate_full_stock_report
from actions.search_trending_stocks import search_trending_stocks
from common.models.export_type import ExportType
from common.models.recommendations import RiskPreference
from common.models.stock_analysis import StockSymbolReport
from config import MAX_REPORT_FETCHING_THREADS, MAX_REPORTS_FOR_RECOMMENDATIONS
from db.get_purchase_recommendations import get_most_recent_purchase_recommendation
from db.get_stock_symbol_reports import get_all_stock_symbol_reports, get_most_recent_stock_symbol_reports
from export.export_reports import export_stock_report, export_purchase_recommendation
from export.export_reports_to_json import export_stock_symbol_report_to_json
from recommendations_generator.get_recommendations import generate_purchase_recommendation

app = typer.Typer()
console = Console()


@app.command()
def generate_stock_report(
        symbols: str = typer.Option(..., help="List of stock symbols separated by commas, like msft,aapl,amzn"),
        days_ago_news: int = typer.Option(5, help="Number of days ago to fetch news"),
        attempt_self_reflexion: bool = typer.Option(True, help="Attempt self reflexion for the report"),
        export_type: str = typer.Option(ExportType.JSON, help="The type of file to export to. "
                                                              "Can be json or pdf")):
    def get_report(stock_symbol: str) -> StockSymbolReport:
        try:
            return generate_full_stock_report(stock_symbol, days_ago_news=days_ago_news,
                                              attempt_self_reflexion=attempt_self_reflexion)
        except Exception as e:
            console.print(f"Error generating stock report for symbol: {stock_symbol}, error: {e}")
            return None

    symbols_list = symbols.split(",")
    # Upper case all symbols
    symbols_list = [symbol.upper().strip() for symbol in symbols_list]
    print(symbols_list)

    console.print(f"Generating stock reports for symbols: {', '.join(symbols_list)}")
    exported_files = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_REPORT_FETCHING_THREADS) as executor:
        futures = [executor.submit(get_report, value) for value in symbols_list]
        results = [future.result() for future in concurrent.futures.as_completed(futures)]
        console.print(f"Finished Generating stock reports for symbols: {', '.join(symbols_list)}")

        for result in results:
            try:
                exported_files.append(export_stock_report(ExportType(export_type.upper()), result))
            except Exception as e:
                console.print(f"Error exporting stock report for symbol: {result.stock_symbol}, error: {e}")
    if exported_files:
        console.print(f"Exported stock reports to files: {exported_files}")


@app.command()
def get_stock_report(latest: bool = typer.Option(True, help="Show only the latest stock report for each symbol"),
                     export_type: str = typer.Option("json", help="Export type, can be json or pdf")):
    if latest:
        reports = get_most_recent_stock_symbol_reports()
    else:
        reports = get_all_stock_symbol_reports()

    exported_files = []
    for report in reports:
        exported_files.append(export_stock_report(ExportType(export_type.upper()), report))

    console.print(f"Exported stock reports to files: {exported_files}")


@app.command()
def generate_recommendation(
        input_file: str = typer.Option(..., help="A file containing the users current state, preferences, etc."),
        risk_preference: str = typer.Option(RiskPreference.MODERATE,
                                            help="The users risk preference. Can be: risky, moderate, safe"),
        export_type: str = typer.Option(ExportType.JSON, help="Export type, can be json or pdf"),
        days_ago_reports: int = typer.Option(2, help="Number of days old to consider reports valid. "
                                                     "Older reports will be ignored.")):
    try:
        current_situation = open(input_file, "r").read()
        console.print(f"Generating recommendations for file: {input_file}")
    except Exception as e:
        console.print(f"Error reading file: {input_file}, error: {e}")
        return
    stock_reports = get_most_recent_stock_symbol_reports()
    stock_reports_by_score = sorted(stock_reports, key=lambda x: x.stock_score, reverse=True)

    stock_reports_by_score = sorted(stock_reports, key=lambda x: x.stock_score, reverse=True)

    valid_timeframe = datetime.now() - timedelta(days=days_ago_reports)
    recent_stock_reports = [report for report in stock_reports_by_score if
                            datetime.strptime(report.timestamp, "%Y-%m-%d %H:%M:%S") >= valid_timeframe]

    reports_after_filtering = recent_stock_reports[:MAX_REPORTS_FOR_RECOMMENDATIONS]

    console.print(
        f"Generating recommendations, considering the"
        f" following symbols: {[report.stock_symbol for report in reports_after_filtering]}")
    recs = generate_purchase_recommendation(reports_after_filtering,
                                            current_situation, RiskPreference(risk_preference.upper()))
    file_name = export_purchase_recommendation(ExportType(export_type.upper()), recs)
    console.print(f"Exported recommendation to file: {file_name}")


@app.command()
def get_latest_recommendation(export_type: str = typer.Option("json", help="Export type, can be json or pdf")):
    recommendation = get_most_recent_purchase_recommendation()
    exported_rec = export_purchase_recommendation(ExportType(export_type.upper()), recommendation)
    console.print(f"Exported recommendation to file: {exported_rec}")


@app.command()
def get_trending_stocks(free_text: Optional[str] = typer.Option(None,
                                                                help="Free text to search for. If not provided, general"
                                                                     " trending stocks will be searched.")):
    console.print(f"Searching for trending stocks with free text: {free_text}")
    trending_stocks = search_trending_stocks(free_text=free_text)
    console.print(f"Trending stocks found: {trending_stocks}")


@app.command()
def run_full_process(
    search_trending: bool = typer.Option(False, help="Search for trending stocks"),
    free_text: Optional[str] = typer.Option(None, help="Free text to search for trending stocks"),
    symbols: Optional[str] = typer.Option(None, help="List of stock symbols separated by commas, like msft,aapl,amzn"),
    input_file: str = typer.Option(..., help="A file containing the user's current state, preferences, etc."),
    export_type: str = typer.Option(ExportType.JSON, help="Export type, can be json or pdf"),
    days_ago_news: int = typer.Option(5, help="Number of days ago to fetch news"),
    risk_preference: str = typer.Option(RiskPreference.MODERATE, help="The user's risk preference. "
                                                                      "Can be: risky, moderate, safe"),
    days_ago_reports: int = typer.Option(2, help="Number of days old to consider reports valid. "
                                                 "Older reports will be ignored.")
):
    # TODO: Yes this is an ugly function, make it better
    if search_trending:
        console.print(f"Searching for trending stocks with free text: {free_text}")
        trending_stocks = search_trending_stocks(free_text=free_text)
        console.print(f"Trending stocks found: {trending_stocks}")

        if symbols is not None:
            symbols += "," + ",".join(trending_stocks)
        else:
            symbols = ",".join(trending_stocks)

    if symbols is None:
        console.print("No stock symbols provided, aborting.")
        return

    # Generate stock reports
    symbols_list = symbols.split(",")
    symbols_list = [symbol.upper().strip() for symbol in symbols_list]
    console.print(f"Generating stock reports for symbols: {symbols_list}")
    exported_files = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_REPORT_FETCHING_THREADS) as executor:
        futures = [executor.submit(generate_full_stock_report, value, days_ago_news, True) for value in symbols_list]
        results = [future.result() for future in concurrent.futures.as_completed(futures)]

        for result in results:
            try:
                exported_files.append(export_stock_report(ExportType(export_type.upper()), result))
            except Exception as e:
                console.print(f"Error exporting stock report for symbol: {result.stock_symbol}, error: {e}")

    if exported_files:
        console.print(f"Exported stock reports to files: {exported_files}")

    # Generate purchase recommendations
    try:
        current_situation = open(input_file, "r").read()
        console.print(f"Generating recommendations for file: {input_file}")
    except Exception as e:
        console.print(f"Error reading file: {input_file}, error: {e}")
        return
    stock_reports = get_most_recent_stock_symbol_reports()
    stock_reports_by_score = sorted(stock_reports, key=lambda x: x.stock_score, reverse=True)

    valid_timeframe = datetime.now() - timedelta(days=days_ago_reports)
    recent_stock_reports = [report for report in stock_reports_by_score if
                            datetime.strptime(report.timestamp, "%Y-%m-%d %H:%M:%S") >= valid_timeframe]

    reports_after_filtering = recent_stock_reports[:MAX_REPORTS_FOR_RECOMMENDATIONS]

    console.print(
        f"Generating recommendations, considering the"
        f" following symbols: {[report.stock_symbol for report in reports_after_filtering]}")
    recs = generate_purchase_recommendation(reports_after_filtering,
                                            current_situation, RiskPreference(risk_preference.upper()))
    file_name = export_purchase_recommendation(ExportType(export_type.upper()), recs)
    console.print(f"Exported recommendation to file: {file_name}")


if __name__ == "__main__":
    app()
