FROM python:3

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

WORKDIR /app
COPY . /app

CMD ["python3", "main.py"]
