from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import json
import requests
import pandas as pd


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

    df['title']
    print(df['title'])
    return ""

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app)
