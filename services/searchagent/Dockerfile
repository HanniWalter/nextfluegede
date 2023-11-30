FROM python:3.10

ENV PYTHONUNBUFFERED 1

WORKDIR /app
COPY requirements.txt requirements.txt 
RUN pip install -r requirements.txt
COPY . .
RUN pip install -r requirements.txt

EXPOSE 5111

CMD ["python3","app.py"]