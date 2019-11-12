FROM python:3.6-slim

WORKDIR /ingest

COPY requirements.txt /ingest

RUN pip install --trusted-host pypi.python.org -r requirements.txt


COPY code/ /ingest

CMD ["python3.6", "-u", "./app.py"]