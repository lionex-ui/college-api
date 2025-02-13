FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y build-essential libpq-dev curl && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml /app/

RUN pip install poetry==1.8.3
RUN poetry config virtualenvs.in-project true
RUN poetry install --no-root

COPY . /app

CMD ["poetry", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
