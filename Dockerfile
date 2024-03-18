FROM node:18-alpine AS build-frontend

WORKDIR /code/atlus

COPY ./atlus/package*.json /code/atlus

RUN npm install

COPY ./atlus /code/atlus

RUN npm run build

FROM python:3.12-slim AS build-api

WORKDIR /code

COPY ./backend/requirements.txt /code/backend/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/backend/requirements.txt

COPY ./backend/app /code/backend/app

COPY --from=build-frontend ./atlus/dist /code/atlus/dist

WORKDIR /code/backend

CMD ["uvicorn", "app.app:app", "--host", "0.0.0.0", "--port", "80"]
