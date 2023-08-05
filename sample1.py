from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import string
import random
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

def generate_short_url():
    letters = string.ascii_letters + string.digits
    return ''.join(random.choice(letters) for _ in range(6))

short_urls = {}

@app.post("/shorten")
def shorten_url(url: URL):
    short_url = generate_short_url()
    short_urls[short_url] = url.longUrl
    return {"shortUrl": f"http://tinyurl.com/api-create.php?{short_url}"}

