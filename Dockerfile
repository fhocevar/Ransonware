FROM python:3.12-slim

RUN groupadd -g 10001 labgroup \
    && useradd -u 10001 -g labgroup -m labuser

WORKDIR /app

RUN pip install --no-cache-dir cryptography==50.0.2

COPY ransomware/ ./ransomware/

USER labuser

ENTRYPOINT ["python", "-m", "ransomware.simulator"]