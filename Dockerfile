FROM python:3.11-slim AS build
WORKDIR /build
COPY requirements.txt .
RUN pip install --root /install --no-compile -r requirements.txt
COPY src/ ./src

FROM python:3.11-slim
WORKDIR /app
COPY --from=build /install/usr/local /usr/local
COPY src/ ./src
COPY config.yaml .

ENTRYPOINT ["python", "src/main.py"]
