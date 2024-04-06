from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import json
import requests
import pandas as pd
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.sentiment import SentimentIntensityAnalyzer
import string
import numpy as np
from scipy.special import softmax

sia = SentimentIntensityAnalyzer()
nltk.download([
     "stopwords",
 ])

# Initialize the stopwords
stop_words = set(stopwords.words('english'))

app = FastAPI()

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=origins,
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

positive_threshold = 0.7
negative_threshold = 0.3

market_to_companies = {
    "tech" : ["meta", "apple", "nvidia", "google", "amazon" ]
}


def preprocess_data(title):
    # Tokenize the title
    words = word_tokenize(title)

    # Remove stopwords and punctuation
    words = [word for word in words if word not in stop_words and word not in string.punctuation]

    # Convert the words to lowercase
    words = [word.lower() for word in words]

    # Join the words back into a string
    preprocessed_title = ' '.join(words)

 
    return preprocessed_title

def preprocess_tokens(title):
        # Tokenize the title
    words = word_tokenize(title)

    # Remove stopwords and punctuation
    words = [word for word in words if word not in stop_words and word not in string.punctuation]

    # Convert the words to lowercase
    words = [word.lower() for word in words]
    return words

# normalize sentiment scores: use the softmax function to 
# convert raw sentiment scores into probabilities, ensuring comparability

def normalize_sentiments(sentiment_data):
    normalized_sentiments = {}
    for key, values in sentiment_data.items():
        # Extract Bloomberg and CNBC sentiment scores
        bloomberg_score = values[0]
        cnbc_score = values[1]

        # Apply softmax normalization
        scores = np.array([bloomberg_score, cnbc_score])
        normalized_scores = softmax(scores)

        # Store normalized scores
        normalized_sentiments[key] = normalized_scores.tolist()

    return normalized_sentiments

""" step 2: Aggregate scores , calculate the average or a weighted average of these
normalized scores across multiple texts, based on their importance"""

def aggregate_scores(normalized_data):
    aggregated_dict = {}
    for key, values in normalized_data.items():
        aggregated_scores = np.mean(values)
        aggregated_dict[key] = aggregated_scores

    return aggregated_dict

def categorize_sentiment(aggregated_scores, positive_threshold, negative_threshold):
    if aggregated_scores[0] >= positive_threshold:
        return 'Positive'
    elif aggregated_scores[0] <= negative_threshold:
        return 'Negative'
    else:
        return 'Neutral'

def fetch_xml_data(url) -> bytes:
    # Get the XML feed URL corresponding to the specified market

    if not url:
        raise HTTPException(status_code=404, detail="XML feed URL not found for market")

    # Fetch the XML data from the URL
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for non-200 status codes
        return response.content  # Return the raw bytes content of the response
    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch XML data: {str(e)}")

@app.get("/")
async def root():
    return { "message" : "Hello world!"}

@app.post("/invest")
async def invest(request: Request):
    """ get the payload and get the strategy and then the market """
    payload = json.loads(await request.body())
    strategy = payload["strategy"]
    market = payload["market"]
    range = payload["range"]

    url_to_feed = {
    f"https://news.google.com/rss/search?q=when:{range}h+allinurl:bloomberg.com&hl=en-US&gl=US&ceid=US:en" : "bloomberg",
    f"https://news.google.com/rss/search?q=when:{range}h+allinurl:cnbc.com&hl=en-US&gl=US&ceid=US:en" : "cnbc"
    }
    market_to_urls = {
        "tech": [f"https://news.google.com/rss/search?q=when:{range}h+allinurl:bloomberg.com&hl=en-US&gl=US&ceid=US:en", f"https://news.google.com/rss/search?q=when:{range}h+allinurl:cnbc.com&hl=en-US&gl=US&ceid=US:en"],
    }

    xml_urls = market_to_urls.get(market)
    companies = market_to_companies.get(market)

    feed_to_headlines = {}

    for url in xml_urls:
        xml = fetch_xml_data(url)
        df = pd.read_xml(xml, xpath=".//item")
        t = df['title'].values
        d = df['pubDate'].values
        preprocessed_titles = [preprocess_data(title) for title in t]
        data = {
            'title': preprocessed_titles,
            'pubDate': d
        }
        new_df = pd.DataFrame(data)
        titles = new_df['title'].values
        dates = new_df['pubDate'].values
        # for each headline, map it to a company
        headlines_to_company = {
            company: [] for company in companies
            }
        print(new_df)
        for company in companies:
            headlines_to_company[company] = []
    
        for title, date in zip(titles, dates):
            # check each of the words and see if they contain any of our companies, if not discard
            tokens = preprocess_tokens(title)
            for token in tokens:
                for company in companies:
                    if token == company:
                        headlines_to_company[company].append({ "headline" : title, 
                                                                "date" : date })
        print(headlines_to_company)
        

        # store it at the dict for that feed
        feed_to_headlines[url_to_feed[url]] = headlines_to_company
    company_to_sentiment = {

    }
    feed_to_company_to_sentiment_date = {
    feed_key: {company: [] for company in companies}
    for feed_key in feed_to_headlines.keys()
}
    print(feed_to_company_to_sentiment_date)
    for company in companies:
        # determine the overall sentiment for it
        # calculate the total sentiment from each rss feed 
        print(company)
        sentiments = []
        for feed in feed_to_headlines:
            headlines = feed_to_headlines[feed][company]
            total_score = 0
            count = 0
            # now calculate the total sentiment for each feed
            for headline in headlines:
                scores = sia.polarity_scores(headline['headline'])["compound"]
                feed_to_company_to_sentiment_date[feed][company].append({ "score" : scores, "date": headline['date'] })
                total_score += scores
                count += 1
            if count == 0:
                avg = 0
            else: 
                avg = total_score / count
            sentiments.append(avg)
            # now with the total score we have the sentiment for that feed
        company_to_sentiment[company] = sentiments
        print(feed_to_company_to_sentiment_date)

    print(company_to_sentiment)

    # now for each company determine the overall sentiment for it 
    return ""

            #  scores = sia.polarity_scores(pre)
            # scores_dict[pre] = scores

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app)
