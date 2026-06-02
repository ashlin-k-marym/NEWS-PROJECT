import requests
import psycopg2
from textblob import TextBlob
from datetime import datetime

API_KEY = "your_api_key"

url = "https://newsapi.org/v2/top-headlines"

params = {
    "country": "us",
    "category": "technology",
    "apiKey": API_KEY
}