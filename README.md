# Yet Another AI Stock Advisor (YAASTA)

Yet Another AI Stock Advisor (yaasta) is a stock recommendation tool that aims to give decent stock purchase recommendations. 

It aims to represent the "reasonable person" that researches companies by reading news, analyzing their financial statements and comparing them to the rest of the market.

This is done by fetching recent news articles about given stocks and fetching their financial statements. Both are then analyzed by OpenAI's GPT3.5 and GPT4 models. The results are then combined with the latest stock price and the stock's market cap to generate a stock symbol report.

Once the user has generated stock symbol reports for the stocks they are interested in, they can generate a stock purchase recommendation by providing a short description of their preferences.



## Features

* Generate full stock symbol reports for given stock symbols
* Generate stock purchase recommendations based on user preferences and existing stock symbol reports
* Search for trending stocks based on latest news articles
* Export reports and recommendations as PDF or JSON

## Output examples:

* [Stock symbol report](docs/StockSymbolReport_Example.pdf) - A report on a single stock symbol
* [Stock purchase recommendation](docs/PurchaseRecommendation_Example.pdf) - A recommendation on which stock to buy based on user preferences and existing stock symbol reports

## Installation

To install yaasta, simply clone the repository and run the following command:

```bash
pip install -r requirements.txt
```

## Getting started

The tool uses the following external services at the moment:
AI Analysis:
* [OpenAI](https://openai.com/) - for generating text using GPT3.5 and GPT4 models

Stock data:
* [Finnhub](https://finnhub.io/) - for fetching stock prices and market caps

News Sources:
* [News API](https://newsapi.org/) - for fetching news articles about given stock symbols
* [Marketaux](https://marketaux.com/) - for fetching financial statements about given stock symbols

You will need to go to the respective websites and create an account to get an API key. With the exception of OpenAI, all have free caps that should be enough to run this tool daily.

Getting the API keys should take around 10 minutes. Once you have done so, create a file locally named `config.json`, and insert the following data there:

```json
{
  "api_keys": {
    "openai_api_key": "<YOUR_OPENAI_API_KEY>",
    "news_api_key": "<YOUR_NEWS_API_KEY>",
    "marketaux_api_key": "<YOUR MARKETAUX_API_KEY>",
    "finnhub_api_key": "<YOUR FINNHUB_API_KEY>"
  },
  "news_sources": ["newsapi", "marketaux"],
  "models": {
    "generating_news_report_model": "GPT_4",
    "generating_stock_symbol_report_model": "GPT_4",
    "generating_purchase_recommendations_model": "GPT_4",
    "summarizing_articles_model": "GPT_35_TURBO",
    "searching_for_trending_stocks_model": "GPT_35_TURBO"
  },
  "reports_and_recommendations": {
    "max_reports": 12
  },
  "directories": {
    "exports_directory": "./exports"
  },
  "database": {
    "db_file": "./sqlite.db",
    "enable_sqlalchemy_logging": false
  },
  "threading": {
    "max_report_fetching_threads": 10
  }
}
```

**NOTE**: At the time of writing, GPT4 API is in beta and not everyone will have access to it. If you do not have access, change all GPT4 items in the config to GPT3.5. You may also do it to save some money in API calls.

Here are some examples of how to use the yaasta CLI:

### Generate current stock reports for specified symbols
```commandline
yaasta generate-stock-report --symbols msft,aapl,amzn --export_type json

// OUTPUT:
Generated stock reports:
  exports/stock_symbol_reports/StockSymbolReport_MSFT-2023-04-25-16:17:55.json
  exports/stock_symbol_reports/StockSymbolReport_AMZN-2023-04-25-16:17:55.json
  exports/stock_symbol_reports/StockSymbolReport_AAPL-2023-04-25-16:17:55.json
```

### Generate a stock recommendation based on user preferences & existing stock reports
```commandline
echo "I like technology and video games and I'm looking to start investing with 1000$" > input.txt
yaasta generate-recommendation --input_file input.txt --export_type pdf

// OUTPUT:
Generated recommendation file: exports/recommendations/PurchaseRecommendation_2023-04-25-16:50:05.pdf
```

### Search for trending stocks
```commandline
yaasta get-trending-stocks --free-text "video games"

// OUTPUT:
Trending stocks:
  ATVI
  EA
  TTWO

```