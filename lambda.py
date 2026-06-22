import os
import json
import boto3
import requests
import pg8000

from datetime import datetime
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# AWS Clients
s3 = boto3.client("s3")

# Sentiment Analyzer
sia = SentimentIntensityAnalyzer()


def get_sentiment(title):
    scores = sia.polarity_scores(title or "")
    compound_score = scores["compound"]

    if compound_score >= 0.05:
        sentiment_label = "Positive"
    elif compound_score <= -0.05:
        sentiment_label = "Negative"
    else:
        sentiment_label = "Neutral"

    return compound_score, sentiment_label


def lambda_handler(event, context):

    api_key = os.environ["NEWS_API_KEY"]
    bucket_name = os.environ["S3_BUCKET"]

    conn = None
    cur = None

    try:
        # Connect to PostgreSQL
        conn = pg8000.connect(
            host=os.environ["DB_HOST"],
            database=os.environ["DB_NAME"],
            user=os.environ["DB_USER"],
            password=os.environ["DB_PASSWORD"],
            port=int(os.environ["DB_PORT"])
        )

        cur = conn.cursor()

        # News API request
        url = "https://newsapi.org/v2/everything"

        params = {
            "q": "AI OR technology OR cloud",
            "language": "en",
            "pageSize": 10,
            "sortBy": "publishedAt",
            "apiKey": api_key
        }

        response = requests.get(
            url,
            params=params,
            timeout=10
        )

        # Handle rate limits
        if response.status_code == 429:
            return {
                "statusCode": 429,
                "body": json.dumps({
                    "error": "NewsAPI rate limit exceeded. Try again later."
                })
            }

        response.raise_for_status()

        news_json = response.json()

        # Save raw JSON to S3
        file_name = (
            f"raw-news/news_"
            f"{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.json"
        )

        s3.put_object(
            Bucket=bucket_name,
            Key=file_name,
            Body=json.dumps(news_json),
            ContentType="application/json"
        )

        articles = news_json.get("articles", [])
        inserted_count = 0

        for article in articles:

            title = article.get("title")
            source_name = article.get("source", {}).get("name")
            published_at = article.get("publishedAt")
            article_url = article.get("url")

            # Convert publication date
            if published_at:
                news_date = datetime.strptime(
                    published_at,
                    "%Y-%m-%dT%H:%M:%SZ"
                ).date()
            else:
                news_date = None

            # Sentiment Analysis
            sentiment_score, sentiment_label = get_sentiment(
                title
            )

            # Insert into PostgreSQL
            cur.execute(
                """
                INSERT INTO news_data
                (
                    news_date,
                    source_name,
                    title,
                    article_url,
                    sentiment_score,
                    sentiment_label
                )
                VALUES (%s, %s, %s, %s, %s, %s)
                ON CONFLICT (article_url)
                DO NOTHING
                """,
                (
                    news_date,
                    source_name,
                    title,
                    article_url,
                    sentiment_score,
                    sentiment_label
                )
            )

            inserted_count += cur.rowcount

        conn.commit()

        return {
            "statusCode": 200,
            "body": json.dumps({
                "message": "News processed successfully",
                "articles_processed": len(articles),
                "articles_inserted": inserted_count,
                "s3_file": file_name
            })
        }

    except Exception as e:

        if conn:
            conn.rollback()

        return {
            "statusCode": 500,
            "body": json.dumps({
                "error": str(e)
            })
        }

    finally:

        if cur:
            cur.close()

        if conn:
            conn.close()