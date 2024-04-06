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

market_to_urls = {
    "tech": ["https://news.google.com/rss/search?q=when:336h+allinurl:bloomberg.com&hl=en-US&gl=US&ceid=US:en",],
}

market_to_companies = {
    "tech" : ["microsoft", "apple", "nvidia", "google", "amazon" ]
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

    xml_urls = market_to_urls.get(market)
    companies = market_to_companies.get(market)

    for url in xml_urls:
        xml = fetch_xml_data(url)
        df = pd.read_xml(xml, xpath=".//item")
        titles = df['title'].values
        # for each headline, map it to a company
        headlines_to_company = {}
        for company in companies:
            headlines_to_company[company] = []
        scores_dict = {}
        for title in titles:
            # tokenize each title
            tokens = preprocess_tokens(title)
            headline = preprocess_data(title)
            # check each of the words and see if they contain any of our companies, if not discard
            for token in tokens:
                for company in companies:
                    if token == company:
                        headlines_to_company[company].append(headline)
            
        print(headlines_to_company)

    return ""

            #  scores = sia.polarity_scores(pre)
            # scores_dict[pre] = scores

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app)
