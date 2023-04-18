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

STOCK INFO: This is the current financial information on the stock:
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
    stock_score: int  # A number from 1 to 10, 10 being the highest score. Essentially gives the stock itself a score.

When writing the confidence level, consider the following:
 - The date / relevance of the data
 - The relation of the data to the stock symbol, especially the news
 - The quality of the data
 - How much the data can actually contribute to choosing whether to buy the stock or not.
 
To calculate the stock_score for any given stock report, you should consider various parameters that contribute to the score in the stock's performance and potential for growth. Each parameter can be assigned a weight based on its importance in determining the overall confidence level. Here's a suggested approach to calculate the confidence_level:

Parameters:

* Acquisition or major partnership (Weight: 0.3): Consider any recent acquisition, merger, or major partnership that could impact the company's growth and position in the industry.

* Financial performance (Weight: 0.25): Analyze the company's recent financial performance, including revenue growth, earnings per share (EPS), and profit margins.

* Legal challenges (Weight: 0.15): Assess the impact of any ongoing legal challenges, including lawsuits and regulatory issues, on the company's operations and reputation.

* Industry outlook (Weight: 0.1): Consider the overall outlook for the industry in which the company operates, including market trends, competition, and potential growth opportunities.

* Analyst recommendations (Weight: 0.1): Take into account the recommendations provided by financial analysts, such as "buy," "hold," or "sell" ratings.

* Stock price and volatility (Weight: 0.1): Analyze the stock's recent price history, including any significant fluctuations and trends, as well as its historical volatility.

Instructions to calculate confidence_level:

* Evaluate each parameter on a scale of 0 (lowest confidence) to 1 (highest confidence), based on the information available in the stock report.

* Multiply each parameter's score by its respective weight.

* Sum the weighted scores to obtain the total confidence_level score.

* Normalize the confidence_level score by dividing it by the sum of the weights, ensuring that it falls between 0 and 1.

Example:

Suppose we have the following scores for each parameter:

Acquisition or major partnership: 0.9
Financial performance: 0.7
Legal challenges: 0.4
Industry outlook: 0.8
Analyst recommendations: 0.6
Stock price and volatility: 0.5
Weighted scores:

Acquisition or major partnership: 0.9 * 0.3 = 0.27
Financial performance: 0.7 * 0.25 = 0.175
Legal challenges: 0.4 * 0.15 = 0.06
Industry outlook: 0.8 * 0.1 = 0.08
Analyst recommendations: 0.6 * 0.1 = 0.06
Stock price and volatility: 0.5 * 0.1 = 0.05
Sum of weighted scores: 0.27 + 0.175 + 0.06 + 0.08 + 0.06 + 0.05 = 0.695

Normalized confidence_level: 0.695 / (0.3 + 0.25 + 0.15 + 0.1 + 0.1 + 0.1) = 0.695

In this example, the stock_score for the given stock report would be 0.695.
 
When writing the confidence explanation, explain why you chose the confidence level you chose, and consider the parameters mentioned above. If something lowered your confidence, explain what it was and what suggestions you have to provide better information.

Your response will contain the JSON and nothing else. The JSON must be valid.
 
"""

GET_STOCK_RECOMMENDATION = """
You are now a financial expert and you will help me decide which stocks to buy. I will provide you with my current
situation which should include my current portfolio, risk preference and any other relevant information. 
I will also provide you with some reports I generated for stocks that I am considering buying. 
You will analyze the reports and provide me with your recommendation. 

The risk preference can be: RISKY, MODERATE, SAFE

Here are some reports on stocks I consider buying:

{stock_reports}

Here is my current situation:

{current_situation}

My risk preference is: {risk_preference}

Here are some relevant objects:

class StockRecommendation(BaseModel):
    symbol: str
    target_price: float
    position: str
    amount: int
    explanation: str


class PurchaseRecommendation(BaseModel):
    stock_recommendations: List[StockRecommendation]
    explanation: str
    confidence_level: int  # A number from 1 to 10, 10 being the highest confidence level. 
    # This is how confident the model is in its recommendation.
    
Your response will be a JSON that fits the PurchaseRecommendation model. The JSON must be valid. In each stock recommendation
you will provide an explanation for your recommendation and consider all the parameters mentioned below.

You may ONLY suggest stocks that are in the stock reports you received. You may NOT suggest stocks that are not in the stock reports.

The explanation in the purchase recommendation should explain why you chose this list of stocks, how confident you are and what factors you considered.

"""

GET_TRENDING_STOCKS = """
You are now a financial expert and you will help me find trending stocks. I will provide you with a few news articles 
relevant to today's date. You will analyze the articles and provide me with a list of trending in the market. 

Here are the articles:
{articles}

Your response will be a JSON List of strings, each string being a stock symbol. The JSON must be valid. For example:

["AAPL", "TSLA", "GOOG"]

The response should contain only the JSON and nothing else.
"""


GET_SEARCH_TERMS_FOR_SELF_REFLEXION = """
You are now a financial expert and you will help me find trending stocks.

Here are suggestions that were provided to improve the confidence level of a stock report:
{confidence_level_suggestions}

You will respond with a JSON list with search queries for news that can improve the stock's confidence level. The search terms will be short and to the point, no more than 4 words each.
The JSON must be valid
For example:
["Microsoft latest acquisition"] 
"""