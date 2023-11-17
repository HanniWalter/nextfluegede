FROM python:3.10

ENV PYTHONUNBUFFERED 1

WORKDIR /app
COPY requirements.txt requirements.txt 
RUN pip install -r requirements.txt
COPY . .
RUN pip install -r requirements.txt

CMD ["python3","main.py"]