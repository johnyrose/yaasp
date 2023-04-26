from typing import Optional

import typer

from yaasp.cli.errors_decorator import exception_handler
from yaasp.cli.generate_recommendation import generate_recommendation_for_file
from yaasp.cli.generate_stock_report_for_symbols import generate_stock_report_for_symbols
from yaasp.cli.get_latest_recommendation_export import get_latest_recommendation_export
from yaasp.cli.get_stock_reports import get_current_stock_reports
from yaasp.cli.get_trending_stocks_search import get_trending_stocks_search
from yaasp.cli.typer_objects import app
from yaasp.common.models.export_type import ExportType


@app.command()
@exception_handler
def generate_recommendation(input_file: str = typer.Option(..., help="A file containing the users current state,"
                                                                     " preferences, etc."),
                            risk_preference: str = typer.Option("moderate", help="The users risk "
                                                                                 "preference. Can be:"
                                                                                 " risky, moderate, safe"),
                            export_type: str = typer.Option('json', help="Export type, can be json or pdf"),
                            days_ago_reports: int = typer.Option(2, help="Number of days old to consider reports "
                                                                         "valid. Older reports will be "
                                                                         "ignored.")) -> None:
    """
    Generate a stock purchase recommendation based on the user's current situation, preferences, and the most recent
    stock reports.
    """
    file_name = generate_recommendation_for_file(input_file, risk_preference, export_type, days_ago_reports)
    if file_name:
        typer.echo(f"Generated recommendation file: {file_name}")
    else:
        typer.echo("Failed to generate recommendation file.")


@app.command()
@exception_handler
def generate_stock_report(symbols: str = typer.Option(..., help="List of stock symbols separated by commas,"
                                                                " like msft,aapl,amzn"),
                          days_ago_news: int = typer.Option(5, help="Number of days ago to fetch news"),
                          attempt_self_reflexion: bool = typer.Option(False, help="Attempt self reflexion"
                                                                                  " for the report"),
                          export_type: str = typer.Option(ExportType.JSON, help="The type of file to "
                                                                                "export to. "
                                                                                "Can be json or pdf")) -> None:
    """
    Generate stock reports for the given symbols, with news and analysis from the specified number of days ago.
    """
    symbol_list = symbols.split(',')
    exported_files = generate_stock_report_for_symbols(symbol_list, days_ago_news, attempt_self_reflexion, export_type)
    if exported_files:
        typer.echo("Generated stock reports:")
        for file in exported_files:
            typer.echo(f"  {file}")
    else:
        typer.echo("Failed to generate stock reports.")


@app.command()
@exception_handler
def get_latest_recommendation(export_type: str = typer.Option("json", help="Export type, can be json or pdf")) -> None:
    """
    Get the most recent stock purchase recommendation and export it to the specified format.
    """
    exported_rec = get_latest_recommendation_export(export_type)
    if exported_rec:
        typer.echo(f"Latest recommendation file: {exported_rec}")
    else:
        typer.echo("Could not find latest recommendation.")


@app.command()
@exception_handler
def get_stock_reports(latest: bool = typer.Option(True, help="Show only the latest stock report for each symbol"),
                      export_type: str = typer.Option("json", help="Export type, can be json or pdf")) -> None:
    """
    Get the current stock reports for all symbols, optionally showing only the latest reports,
     and export them to the specified format.
    """
    exported_files = get_current_stock_reports(latest, export_type)
    if exported_files:
        typer.echo("Generated stock reports:")
        for file in exported_files:
            typer.echo(f"  {file}")
    else:
        typer.echo("No reports were found.")


@app.command()
@exception_handler
def get_trending_stocks(free_text: Optional[str] = typer.Option(None, help="Free text"
                                                                           " to search for. If not provided, "
                                                                           "general trending stocks will be "
                                                                           "searched.")) -> None:
    """
    Get current trending stocks, optionally searching for a specific free text.
    """
    trending_stocks = get_trending_stocks_search(free_text)
    if trending_stocks:
        typer.echo("Trending stocks:")
        for stock in trending_stocks:
            typer.echo(f"  {stock}")
    else:
        typer.echo("No trending stocks found.")


@app.callback()
@exception_handler
def main(ctx: typer.Context):
    """
    Your Automated Stock Advisor and Portfolio Strategist (Y.A.A.S.P.) is a command-line tool that provides
    stock recommendations, generates stock reports, and assists with portfolio management.
    """
    if ctx.invoked_subcommand is None:
        typer.echo(ctx.get_help())
        raise typer.Exit()


if __name__ == "__main__":
    app()
