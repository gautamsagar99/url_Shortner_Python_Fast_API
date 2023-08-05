from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests
from urllib.parse import urlencode
from fastapi.staticfiles import StaticFiles
from starlette.responses import HTMLResponse

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class URL(BaseModel):
    longUrl: str


def create_short_url(long_url):
    api_url = "http://tinyurl.com/api-create.php"
    payload = {"url": long_url}
    headers = {"Content-Type": "application/x-www-form-urlencoded"}

    try:
        response = requests.post(api_url, data=urlencode(payload), headers=headers)
        if response.status_code == 200:
            short_url = response.text
            return short_url
        else:
            print("Error:", response.status_code)
    except requests.exceptions.RequestException as e:
        print("Error:", e)



# Mount the static files directory to serve the HTML file
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def get_index():
    # Serve the index.html file
    with open("static/index.html", "r") as f:
        content = f.read()
    return HTMLResponse(content)

@app.post("/shorten")
def shorten_url(url: URL):
    short_url = create_short_url(url.longUrl)
    return {"shortUrl": short_url}
