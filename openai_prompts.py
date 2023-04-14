GET_ARTICLE_SUMMARY_PROMPT = """
This is an article written about a company named {company_name}. You will summarize it in 2 paragraphs, each being 
about 5-6 sentences. Try to lose as little information as possible. If the article contains info about more companies, 
you can add them to the summary, but make sure that the summary focuses on the provided company.

{title}

{content}
"""


GET_ARTICLE_NEWS_REPORT = """
You are now a financial expert and you will provide assistance to a financial analyst. Here are summaries of news about 
the {stock_symbol} stock:

{article_summaries}

You will properly analyze the summaries and respond with a JSON with the following keys:

- "general_sentiment": <VERY POSITIVE / POSITIVE / NEUTRAL / NEGATIVE / VERY NEGATIVE>,
- "sentiment_reason": <1 sentence that explains why you chose the sentiment>,
- "financial_information": <1 sentence that explains the financial information you found in the summaries that could be interesting>,
- "news_summary": <A 3-paragraph (each paragraph 2-3 sentences) summary of all the news about the company that you received. Include any interesting information to a financial analyst if you find any >
- "stock_symbol": <The stock symbol of the company you are analyzing>

Respond with only the JSON object and nothing else.
"""

GET_FULL_STOCK_REPORT = """
You are now a financial expert and you will provide assistance to a financial analyst.

Today is {date} and you will provide a full report on the {stock_symbol} stock.
 
Here is some information about the {stock_symbol} stock:

STOCK INFO: This is the current information on the stock:
{stock_info}

NEWS: Here is a summary of the news that was published about the {stock_symbol} stock recently:
{news_summary}

You will analyze the provided information and make your recommendation. You will respond with a JSON with the following fields:

    stock_symbol: str
    news_report: StockNewsReport  # The news report for the stock symbol
    data: Dict  # The data for the stock symbol
    stock_recommendation: StockRecommendation  # The recommendation for the stock
    stock_recommendation_reason: str  # The reason for the stock recommendation
    position_recommendation: PositionRecommendation  # The recommendation for the position
    position_recommendation_reason: str  # The reason for the position recommendation
    amount_suggested: int  # The amount of stocks suggested to buy/sell

Here are the relevant objects:

class StockRecommendation(str, enum.Enum):
    BUY = "BUY"
    HOLD = "HOLD"
    SELL = "SELL"


class PositionRecommendation(str, enum.Enum):
    LONG = "Long"  # Suggest entering a long position for the stock
    SHORT = "Short"  # Suggest entering a short position for the stock
    NONE = "None"  # Suggest not to enter any position for the stock


class GeneralSentiment(str, enum.Enum):
    VERY_POSITIVE = "VERY POSITIVE"
    POSITIVE = "POSITIVE"
    NEUTRAL = "NEUTRAL"
    NEGATIVE = "NEGATIVE"
    VERY_NEGATIVE = "VERY NEGATIVE"


class StockNewsReport(BaseModel):
    stock_symbol: str
    news_summary: str
    financial_information: str  # Any interesting points that can be gathered specifically in the financial sector
    general_sentiment: GeneralSentiment
    sentiment_reason: str


class StockSymbolReport(BaseModel):
    stock_symbol: str
    news_report: StockNewsReport  # The news report for the stock symbol
    data: Dict  # The data for the stock symbol
    stock_recommendation: StockRecommendation  # The recommendation for the stock
    stock_recommendation_reason: str  # The reason for the stock recommendation
    position_recommendation: PositionRecommendation  # The recommendation for the position
    position_recommendation_reason: str  # The reason for the position recommendation
    amount_suggested: int  # The amount of stocks suggested to buy/sell

Your response will contain the JSON and nothing else.
 
"""