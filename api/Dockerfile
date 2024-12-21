FROM python:3.8-slim as builder

WORKDIR /build
RUN apt-get update && \
    apt-get install -y dos2unix

COPY . .
RUN dos2unix entrypoint.sh healthcheck.sh && \
    chmod +x entrypoint.sh healthcheck.sh

FROM python:3.8-slim

RUN apt-get update && \
    apt-get install -y postgresql-client curl && \
    pip install --upgrade pip

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY --from=builder /build .

EXPOSE 5000

ENTRYPOINT ["/bin/sh"]
CMD ["/app/entrypoint.sh"]