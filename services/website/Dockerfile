FROM python:3.10

ENV PYTHONUNBUFFERED 1

WORKDIR /app
copy . . 
RUN pip install -r requirements.txt
EXPOSE 5101

CMD ["python3","app.py"]


