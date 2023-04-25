import concurrent.futures
from datetime import datetime, timedelta
from typing import Optional

import typer

from src.actions import generate_full_stock_report
from src.actions import search_trending_stocks
from src.cli.generate_recommendation import generate_recommendation_for_file
from src.cli.generate_stock_report_for_symbols import generate_stock_report_for_symbols
from src.cli.get_latest_recommendation_export import get_latest_recommendation_export
from src.cli.get_stock_reports import get_current_stock_reports
from src.cli.get_trending_stocks_search import get_trending_stocks_search
from src.cli.typer_objects import app, console
from src.common.models.export_type import ExportType
from src.common.models.recommendations import RiskPreference
from config import MAX_REPORT_FETCHING_THREADS, MAX_REPORTS_FOR_RECOMMENDATIONS
from src.db.get_stock_symbol_reports import get_most_recent_stock_symbol_reports
from src.export.export_reports import export_stock_report, export_purchase_recommendation
from src.recommendations_generator.generate_recommendation import generate_purchase_recommendation


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


if __name__ == "__main__":
    app()

# 10.84
