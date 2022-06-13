FROM python:3.8

COPY ./email-parser/requirements.txt /requirements.txt

RUN pip install -r requirements.txt

COPY ./email-parser/app /app

WORKDIR /app

CMD ["uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "5000"]