import concurrent.futures
from datetime import datetime, timedelta
from typing import Optional

import typer
from rich.console import Console

from actions.generate_full_stock_report import generate_full_stock_report
from actions.search_trending_stocks import search_trending_stocks
from cli.generate_recommendation import generate_recommendation_for_file
from cli.generate_stock_report_for_symbols import generate_stock_report_for_symbols
from cli.get_latest_recommendation_export import get_latest_recommendation_export
from cli.get_stock_reports import get_current_stock_reports
from cli.get_trending_stocks_search import get_trending_stocks_search
from cli.typer_objects import app, console
from common.models.export_type import ExportType
from common.models.recommendations import RiskPreference
from config import MAX_REPORT_FETCHING_THREADS, MAX_REPORTS_FOR_RECOMMENDATIONS
from db.get_stock_symbol_reports import get_most_recent_stock_symbol_reports
from export.export_reports import export_stock_report, export_purchase_recommendation
from recommendations_generator.generate_recommendation import generate_purchase_recommendation


@app.command()
def generate_recommendation(input_file: str = typer.Option(..., help="A file containing the users current state,"
                                                                     " preferences, etc."),
                            risk_preference: str = typer.Option(RiskPreference.MODERATE, help="The users risk "
                                                                                              "preference. Can be:"
                                                                                              " risky, moderate, safe"),
                            export_type: str = typer.Option(ExportType.JSON, help="Export type, can be json or pdf"),
                            days_ago_reports: int = typer.Option(2, help="Number of days old to consider reports "
                                                                         "valid. Older reports will be "
                                                                         "ignored.")) -> None:
    file_name = generate_recommendation_for_file(input_file, risk_preference, export_type, days_ago_reports)
    if file_name:
        typer.echo(f"Generated recommendation file: {file_name}")
    else:
        typer.echo("Failed to generate recommendation file.")


@app.command()
def generate_stock_report(symbols: str = typer.Option(..., help="List of stock symbols separated by commas,"
                                                                " like msft,aapl,amzn"),
                          days_ago_news: int = typer.Option(5, help="Number of days ago to fetch news"),
                          attempt_self_reflexion: bool = typer.Option(False, help="Attempt self reflexion"
                                                                                  " for the report"),
                          export_type: str = typer.Option(ExportType.JSON, help="The type of file to "
                                                                                "export to. "
                                                                                "Can be json or pdf")) -> None:
    symbol_list = symbols.split(',')
    exported_files = generate_stock_report_for_symbols(symbol_list, days_ago_news, attempt_self_reflexion, export_type)
    if exported_files:
        typer.echo("Generated stock reports:")
        for file in exported_files:
            typer.echo(f"  {file}")
    else:
        typer.echo("Failed to generate stock reports.")


@app.command()
def get_latest_recommendation(export_type: str = typer.Option("json", help="Export type, can be json or pdf")) -> None:
    exported_rec = get_latest_recommendation_export(export_type)
    if exported_rec:
        typer.echo(f"Latest recommendation file: {exported_rec}")
    else:
        typer.echo("Could not find latest recommendation.")


@app.command()
def get_stock_reports(latest: bool = typer.Option(True, help="Show only the latest stock report for each symbol"),
                      export_type: str = typer.Option("json", help="Export type, can be json or pdf")) -> None:
    exported_files = get_current_stock_reports(latest, export_type)
    if exported_files:
        typer.echo("Generated stock reports:")
        for file in exported_files:
            typer.echo(f"  {file}")
    else:
        typer.echo("No reports were found.")


@app.command()
def get_trending_stocks(free_text: Optional[str] = typer.Option(None, help="Free text"
                                                                           " to search for. If not provided, "
                                                                           "general trending stocks will be "
                                                                           "searched.")) -> None:
    trending_stocks = get_trending_stocks_search(free_text)
    if trending_stocks:
        typer.echo("Trending stocks:")
        for stock in trending_stocks:
            typer.echo(f"  {stock}")
    else:
        typer.echo("No trending stocks found.")


@app.command()
def run_full_process(
        search_trending: bool = typer.Option(False, help="Search for trending stocks"),
        free_text: Optional[str] = typer.Option(None, help="Free text to search for trending stocks"),
        symbols: Optional[str] = typer.Option(None,
                                              help="List of stock symbols separated by commas, like msft,aapl,amzn"),
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

# 10.84
