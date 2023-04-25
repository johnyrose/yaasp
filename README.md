# Yet Another AI Stock Screener (YAASC)

Yet Another AI Stock Screener (YAASC) is an intelligent stock recommendation tool that leverages the power of OpenAI to provide personalized stock purchase suggestions based on a user's preferences and the most recent market data. By fetching recent news, summarizing, and analyzing them, YAASC delivers a comprehensive report on selected stocks, helping users make informed decisions on their investments.

## Features

- Generate stock purchase recommendations based on user preferences and the latest stock reports
- Create stock reports with news and analysis for specified stock symbols
- Export recommendations and stock reports in JSON and PDF formats
- Retrieve the latest stock purchase recommendation
- Retrieve stock reports for all available symbols or the latest ones
- Search for trending stocks

## Installation

To install YAASC, simply clone the repository and run the following command:

```bash
pip install -r requirements.txt
```

## Quickstart

Here are some examples of how to use the YAASC CLI:

### Generate current stock reports for specified symbols
```commandline
yaasc generate-stock-report --symbols msft,aapl,amzn --export_type json
```

### Generate a stock recommendation based on user preferences & existing stock reports
```commandline
echo "I like technology and video games and I'm looking to start investing with 1000$" > input.txt
yaasc generate-recommendation --input_file input.txt --export_type json
```

### Search for trending stocks
```commandline
yaasc get_trending_stocks --free_text "electric vehicles"
```