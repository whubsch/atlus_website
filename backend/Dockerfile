FROM python:3.11-slim

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./app /code/app

EXPOSE 5000

CMD ["uvicorn", "app.app:app", "--host", "0.0.0.0", "--port", "5000"]
