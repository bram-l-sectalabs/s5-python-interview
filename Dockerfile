FROM python:3.11-slim

RUN pip install pipenv

WORKDIR /app

COPY Pipfile* ./

RUN pipenv install --system --deploy

COPY . .

EXPOSE 8000

CMD ["fastapi", "run", "main.py"]
