FROM python:3.11-slim

RUN pip install pipenv

WORKDIR /app

COPY Pipfile* ./

COPY /tmp/server.key ./
COPY /tmp/server.crt ./

RUN pipenv install --system --deploy

COPY . .

EXPOSE 8000

CMD ["python", "app.py"]
