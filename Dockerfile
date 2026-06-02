FROM python:3.11

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir \
    streamlit \
    pandas \
    plotly \
    sqlalchemy \
    psycopg2-binary \
    requests \
    textblob

EXPOSE 8501

CMD ["streamlit", "run", "dashboard.py", "--server.address=0.0.0.0"]