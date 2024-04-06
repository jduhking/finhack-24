from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import json
import requests
import pandas as pd
import nltk
from pprint import pprint
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.sentiment import SentimentIntensityAnalyzer
import string

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

market_to_url = {
    "tech": "https://news.google.com/rss/search?q=when:24h+allinurl:bloomberg.com&hl=en-US&gl=US&ceid=US:en",
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


def fetch_xml_data(market: str) -> bytes:
    # Get the XML feed URL corresponding to the specified market
    xml_url = market_to_url.get(market)

    if not xml_url:
        raise HTTPException(status_code=404, detail="XML feed URL not found for market")

    # Fetch the XML data from the URL
    try:
        response = requests.get(xml_url)
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

    xml = fetch_xml_data(market)
    
    df = pd.read_xml(xml, xpath=".//item")

    titles = df['title'].values
    scores_dict = {}
    for title in titles:
        # tokenize each title
        pre = preprocess_data(title)
        # get the score
        scores = sia.polarity_scores(pre)
        scores_dict[pre] = scores
    print(scores_dict)

    return scores_dict

 

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app)
