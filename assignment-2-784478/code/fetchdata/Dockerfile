FROM python:3.6-slim

EXPOSE 8000
WORKDIR /fetch

COPY requirements.txt /fetch

RUN pip install --trusted-host pypi.python.org -r requirements.txt


COPY code/ /fetch

CMD ["python3.6", "-u", "./app.py"]