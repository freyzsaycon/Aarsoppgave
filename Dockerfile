FROM python:3.11

WORKDIR /app

COPY . .

RUN pip install flask mysql-connector-python python-dotenv

EXPOSE 5000

CMD ["python", "app.py"]