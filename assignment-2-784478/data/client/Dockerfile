FROM python:3.6-slim

WORKDIR /client

COPY requirements.txt /client

RUN pip install --trusted-host pypi.python.org -r requirements.txt


COPY code/ /client

CMD ["python3.6", "-u", "./app.py"]