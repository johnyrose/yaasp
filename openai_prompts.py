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
- "articles_summary": A list of shortened summaries for each article. Each item in the list will be of the following structure:
class ArticleSummary(BaseModel):
    summary: str
    date: str  # The publication date of the article

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


Here some relevant objects:

class StockRecommendation(str, enum.Enum):
    BUY = "BUY"
    HOLD = "HOLD"
    SELL = "SELL"


class PositionRecommendation(str, enum.Enum):
    LONG = "LONG"  # Suggest entering a long position for the stock
    SHORT = "SHORT"  # Suggest entering a short position for the stock
    NONE = "NONE"  # Suggest not to enter any position for the stock


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

You will analyze the provided information about the stock symbol and make your recommendation. You will respond with a JSON with the following fields:

    stock_symbol: str
    stock_recommendation: StockRecommendation  # The recommendation for the stock
    stock_recommendation_reason: str  # The reason for the stock recommendation
    position_recommendation: PositionRecommendation  # The recommendation for the position
    position_recommendation_reason: str  # The reason for the position recommendation
    confidence_level: int  # A number from 1 to 10, 10 being the highest confidence level. This is how confident the model is in its recommendation.
    confidence_explanation: str  # An explanation of the confidence level

When writing the confidence level, consider the following:
 - The date / relevance of the data
 - The relation of the data to the stock symbol, especially the news
 - The quality of the data
 - How much the data can actually contribute to choosing whether to buy the stock or not.
 
When writing the confidence explanation, explain why you chose the confidence level you chose, and consider the parameters mentioned above. If something lowered your confidence, explain what it was and what suggestions you have to provide better information.

Your response will contain the JSON and nothing else. The JSON must be valid.
 
"""