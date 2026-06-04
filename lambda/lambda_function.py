import os
import requests
import pg8000
from datetime import datetime

def get_sentiment(title):
    positive_words = ["good", "great", "growth", "success", "win", "positive", "rise", "boost", "profit"]
    negative_words = ["bad", "loss", "fail", "crash", "negative", "fall", "risk", "drop", "war"]

    text = title.lower()

    score = 0
    for word in positive_words:
        if word in text:
            score += 1

    for word in negative_words:
        if word in text:
            score -= 1

    if score > 0:
        return score, "Positive"
    elif score < 0:
        return score, "Negative"
    else:
        return score, "Neutral"

def lambda_handler(event, context):
    api_key = os.environ["NEWS_API_KEY"]

    conn = pg8000.connect(
        host=os.environ["DB_HOST"],
        database=os.environ["DB_NAME"],
        user=os.environ["DB_USER"],
        password=os.environ["DB_PASSWORD"],
        port=int(os.environ["DB_PORT"])
    )

    url = "https://newsapi.org/v2/top-headlines"

    params = {
        "q": "AI OR technology OR cloud",
        "language": "en",
        "pageSize": 20,
        "apiKey": api_key
    }

    response = requests.get(url, params=params)
    articles = response.json().get("articles", [])

    cur = conn.cursor()

    for article in articles:
        title = article.get("title")
        source_name = article.get("source", {}).get("name")
        published_at = article.get("publishedAt")

        if published_at:
            news_date = datetime.strptime(published_at, "%Y-%m-%dT%H:%M:%SZ").date()
        else:
            news_date = None

        sentiment_score, sentiment_label = get_sentiment(title or "")

        cur.execute("""
            INSERT INTO news_data
            (news_date, source_name, title, sentiment_score, sentiment_label)
            VALUES (%s, %s, %s, %s, %s)
        """, (
            news_date,
            source_name,
            title,
            sentiment_score,
            sentiment_label
        ))

    conn.commit()
    cur.close()
    conn.close()

    return {
        "statusCode": 200,
        "body": f"{len(articles)} articles inserted successfully"
    }