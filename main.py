import json

from actions.generate_full_stock_report import generate_stock_report


if __name__ == '__main__':
    symbols = ["BBBY", "AAPL", "TSLA", "AMZN", "MSFT", "GOOG", "VOO", "INTC", "AMD", "EA"]
    for symbol in symbols:
        try:
            report = generate_stock_report(symbol)
            with open(f'stock_report_{symbol}.json', 'w') as f:
                f.write(json.dumps(report.dict(), indent=4))
            print(report.dict())
        except Exception as e:
            print(f'Failed to generate report for {symbol} with error: {e}')

# TODO:
# Add more news sources
# About the investor & their interests & financial situation before recommending numbers.
