# Yet Another AI Stock Advisor (YAASTA)

Yet Another AI Stock Advisor (yaasta) is a stock recommendation tool that aims to give decent stock purchase recommendations. 

It aims to represent the "reasonable person" that researches companies by reading news, analyzing their financial statements and comparing them to the rest of the market.

This is done by fetching recent news articles about given stocks and fetching their financial statements. Both are then analyzed by OpenAI's GPT3.5 and GPT4 models. The results are then combined with the latest stock price and the stock's market cap to generate a stock symbol report.

Once the user has generated stock symbol reports for the stocks they are interested in, they can generate a stock purchase recommendation by providing a short description of their preferences.


This is basically my attempt at reading the stock market using AI. 

### An obvious but needed disclaimer

I am not a financial advisor, and this tool is not meant to be used as a financial advisor. This is nothing more than a fun side project that I am working on in my free time.

## Table of contents

* [Features](#features)
* [Output examples](#output-examples)
* [Flow diagrams](#flow-diagrams)
* [Installation](#installation)
* [Getting started](#getting-started)
* [Commands](#commands)
* [Quick video usage examples](#quick-video-usage-examples)
* [Final notes](#final-notes)

## Features

* Generate full stock symbol reports for given stock symbols
* Generate stock purchase recommendations based on user preferences and existing stock symbol reports
* Search for trending stocks based on latest news articles
* Export reports and recommendations as PDF or JSON 

## Output examples:

* JSON:
  * [Stock symbol report](docs/StockSymbolReport_example.json) - A JSON report on a single stock symbol
  * [Stock purchase recommendation](docs/PurchaseRecommendation_example.json) - A JSON recommendation on which stock to buy based on user preferences and existing stock symbol reports
* PDF:
  * [Stock symbol report](docs/StockSymbolReport_Example.pdf) - A PDF report on a single stock symbol
  * [Stock purchase recommendation](docs/PurchaseRecommendation_example.pdf) - A PDF recommendation on which stock to buy based on user preferences and existing stock symbol reports

## Flow diagrams:

* **Generating stock symbol report:**

![getting-stock-report](https://user-images.githubusercontent.com/26342860/234531794-e9c0f6f9-357c-43c2-bd0c-8815f0b33aa8.PNG)

* **Generating purchase recommendation:**

![recommendation](https://user-images.githubusercontent.com/26342860/234533575-7071044b-23fe-4491-a46a-14d7a21c71ea.PNG)



## Installation

To install yaasta, simply clone the repository and run the following command:

```bash
pip install -r requirements.txt
```

## Getting started

The tool uses the following external services at the moment:

**AI Analysis:**
* [OpenAI](https://openai.com/) - for generating text using GPT3.5 and GPT4 models

**Stock data:**
* [Finnhub](https://finnhub.io/) - for fetching stock prices and market caps

**News Sources:**
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

### Saved information

* All the reports are saved to a local SQLITE database.
* Any command that generates reports will export them to the `exports` directory. which will be created if it does not exist.

Here are some examples of how to use the yaasta CLI:


## Commands
### Show the help message
```commandline
python main.py --help

# OUTPUT:

 Usage: main.py [OPTIONS] COMMAND [ARGS]...

╭─ Options ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --install-completion        [bash|zsh|fish|powershell|pwsh]  Install completion for the specified shell. [default: None]                                                                   │
│ --show-completion           [bash|zsh|fish|powershell|pwsh]  Show completion for the specified shell, to copy it or customize the installation. [default: None]                            │
│ --help                                                       Show this message and exit.                                                                                                   │
╰────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Commands ─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ generate-recommendation         Generate a stock purchase recommendation based on the user's current situation, preferences, and the most recent stock reports.                            │
│ generate-stock-report           Generate stock reports for the given symbols, with news and analysis from the specified number of days ago.                                                │
│ get-latest-recommendation       Get the most recent stock purchase recommendation and export it to the specified format.                                                                   │
│ get-stock-reports               Get the current stock reports for all symbols, optionally showing only the latest reports, and export them to the specified format.                        │
│ get-trending-stocks             Get current trending stocks, optionally searching for a specific free text.                                                                                │
╰────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

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

* Once you generated stock symbol reports, you can use them & your preferences to generate a purchase recommendation.
* You'll need to create a local text file, and write your preferences there
* These preferences are, essentially, anything you want the AI to know when recommending stocks for you. I would suggest including:
  * Your current portfolio
  * Your budget
  * Industries you prefer
  * Your investment goals (e.g. long term, short term, etc.)
  * For example:
  ```text
    input.txt:
  
    Here is my current portfolio:
    "Symbol","Description","Quantity","MarkPrice","FifoPnlUnrealized","OpenPrice","ReportDate"
    "AAPL","APPLE INC","1","165.33","-1.45","166.78","2023-04-24"
    "AMD","ADVANCED MICRO DEVICES","5","87.57","-33.5","94.27","2023-04-24"
    "AMZN","AMAZON.COM INC","20","106.21","-0.3","106.225","2023-04-24"
    "GOOGL","ALPHABET INC-CL A","9","105.97","-3.044","106.308222222","2023-04-24"
    "INTC","INTEL CORP","10","29.66","-35.55","33.215","2023-04-24"
    "MSFT","MICROSOFT CORP","2","281.77","-9.66","286.6","2023-04-24"
    "NVDA","NVIDIA CORP","4","270.42","-13.78","273.865","2023-04-24"
    
    I am looking to invest in the long run. I don't care for short term gains. I have 2000 USD to invest

  ```

```commandline
yaasta generate-recommendation --input_file input.txt --export_type pdf

# OUTPUT:
Generated recommendation file: exports/recommendations/PurchaseRecommendation_2023-04-25-16:50:05.pdf
```

### Search for trending stocks

```commandline
yaasta get-trending-stocks --free-text "video games"

# OUTPUT:
Trending stocks:
  ATVI
  EA
  TTWO

```

### Fetching existing data

You can use the `get-stock-reports` and `get-latest-recommendation` commands to fetch existing data from the database.

```commandline
yaasta get-stock-reports --export-type json
# OUTPUT:
Generated stock reports:
  exports/stock_symbol_reports/StockSymbolReport_MSFT-2023-04-25-16:17:55.json
  exports/stock_symbol_reports/StockSymbolReport_AMZN-2023-04-25-16:17:55.json
  exports/stock_symbol_reports/StockSymbolReport_AAPL-2023-04-25-16:17:55.json
```

```commandline
yaasta get-latest-recommendation --export-type pdf
# OUTPUT:
Generated recommendation file: exports/recommendations/PurchaseRecommendation_2023-04-25-16:50:05.pdf 
```

  

## Quick Video usage examples

* Generating stock reports:

https://user-images.githubusercontent.com/26342860/234519340-77b056ee-c5df-4f8c-9c94-00a2b73820fd.mp4

* Generating stock recommendation:

https://user-images.githubusercontent.com/26342860/234519432-e4a13ecf-10e4-415e-b45f-88600a760e64.mp4

* Getting trending stocks:

https://user-images.githubusercontent.com/26342860/234519503-3f4b8961-133f-4150-b119-546b9ffef5ae.mp4


### Final notes

Thank you very much for checking it out! This was a fun side project to make. I hope you find it useful and I'm always open for feedback and suggestions.
