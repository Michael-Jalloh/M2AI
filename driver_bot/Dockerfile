FROM rasa/rasa-sdk:2.8.1

COPY requirements.txt .

USER root

RUN pip install --no-cache-dir -r requirements.txt

USER 1001