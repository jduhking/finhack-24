from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import json
import requests
from lxml import etree


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def fetch_xml_data(market: str) -> str:
    # this function will fetch the xml data depending on the market
    market_to_url = {
        "tech": "https://news.google.com/rss/search?q=when:24h+allinurl:bloomberg.com&hl=en-US&gl=US&ceid=US:en",
    }
    # get the xml feed url corresponding to the specified market

    xml_url = market_to_url(market)

    if not xml_url:
        raise HTTPException(status_code=404, detail="XML feed URL not found for market")
    
    # fetch the XML data from the URL

    response = requests.get(xml_url)

    if response.status_code != 200:
        raise HTTPException(status_code=500, detail=f"Failed to fetch XML data: { response.text }")
    
    return response.content

@app.get("/")
async def root():
    return { "message" : "Hello world!"}

@app.post("/invest")
async def invest(request: Request):
    """ get the payload and get the strategy and then the market """
    payload = json.loads(await request.body())
    print(payload)


