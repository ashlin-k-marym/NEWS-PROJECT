# News Sentiment Analytics Pipeline using AWS, PostgreSQL, and Streamlit

## Project Overview

This project is an end-to-end Data Engineering and Analytics solution that collects real-time technology news articles from NewsAPI, performs sentiment analysis using TextBlob, stores the processed data in PostgreSQL (AWS RDS), and visualizes insights through an interactive Streamlit dashboard.

The pipeline demonstrates key data engineering concepts including data ingestion, transformation, storage, analytics, and cloud deployment.

---

## Architecture

NewsAPI → Python ETL Script → Sentiment Analysis (TextBlob) → PostgreSQL (AWS RDS) → Streamlit Dashboard → Docker → AWS ECS Fargate

---

## Features

* Fetches latest technology news from NewsAPI
* Performs sentiment analysis on article headlines
* Classifies sentiment as Positive, Negative, or Neutral
* Stores processed data in PostgreSQL
* Displays analytics through Streamlit dashboard
* Color-coded sentiment scores
* Real-time data refresh
* Dockerized application for deployment
* Cloud-ready architecture using AWS services

---

## Tech Stack

### Data Ingestion

* Python
* Requests
* NewsAPI

### Data Processing

* TextBlob
* Pandas
* NumPy

### Database

* PostgreSQL
* AWS RDS
* SQLAlchemy
* Psycopg2

### Dashboard

* Streamlit
* Plotly

### Cloud & Deployment

* AWS RDS
* Docker
* AWS ECS Fargate

---

## Database Schema

### news_data

| Column          | Type               |
| --------------- | ------------------ |
| id              | SERIAL PRIMARY KEY |
| news_date       | DATE               |
| source_name     | VARCHAR(255)       |
| title           | TEXT               |
| sentiment_score | FLOAT              |
| sentiment_label | VARCHAR(20)        |
| created_at      | TIMESTAMP          |

---

## ETL Workflow

### Extract

* Connect to NewsAPI
* Retrieve latest technology news articles
* Parse article metadata

### Transform

* Extract headline text
* Calculate sentiment polarity using TextBlob
* Generate sentiment labels:

  * Positive
  * Negative
  * Neutral

### Load

* Store processed records in PostgreSQL
* Commit transactions to AWS RDS

---

## Dashboard Features

### News View

* Displays latest news articles
* Shows source information
* Displays sentiment scores
* Shows sentiment labels

### Analytics View

* Sentiment distribution analysis
* Positive vs Negative trend visualization
* Interactive charts using Plotly

### Additional Features

* Latest update timestamp
* Responsive dashboard layout
* Color-coded sentiment scores

---

## Installation

### Clone Repository

```bash
git clone <repository-url>
cd news-sentiment-analytics
```

### Create Virtual Environment

```bash
python -m venv venv
```

### Activate Environment

Windows:

```bash
venv\Scripts\activate
```

Linux/Mac:

```bash
source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Configuration

Create a `.env` file:

```env
NEWS_API_KEY=your_api_key

DB_HOST=your_rds_endpoint
DB_NAME=news_db
DB_USER=postgres
DB_PASSWORD=your_password
DB_PORT=5432
```

---

## Running the ETL Pipeline

```bash
python news_pipeline.py
```

---

## Running the Dashboard

```bash
streamlit run dashboard.py
```

---

## Docker Deployment

### Build Image

```bash
docker build -t news-dashboard .
```

### Run Container

```bash
docker run -p 8501:8501 news-dashboard
```

---

## AWS Services Used

* AWS RDS (PostgreSQL)
* AWS ECS Fargate
* Docker
* Amazon ECR (Optional)

---

## Project Outcomes

* Automated news ingestion pipeline
* Real-time sentiment analytics
* Cloud-hosted PostgreSQL storage
* Interactive business intelligence dashboard
* Production-ready containerized deployment

---

## Future Enhancements

* Multi-category news support
* Scheduled ingestion using AWS Lambda
* Event-driven orchestration with EventBridge
* Raw data storage in Amazon S3
* Advanced NLP models for sentiment analysis
* Real-time streaming analytics

---

## Author

ASHLIN K

Data Engineering | AWS | Python | PostgreSQL | Streamlit