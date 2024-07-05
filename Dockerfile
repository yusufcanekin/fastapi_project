FROM python:3.8

WORKDIR /fastapi-app

COPY requirements.txt .

RUN pip install -r requirements.txt

EXPOSE 8000

COPY ./app .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]