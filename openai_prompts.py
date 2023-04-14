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