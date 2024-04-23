FROM python:3.11.8-slim

WORKDIR /app

RUN pip install pdm
COPY pyproject.toml pdm.lock ./
RUN pdm install --prod

COPY src ./src
COPY main.py ./

ENTRYPOINT ["/app/.venv/bin/python", "main.py"]
