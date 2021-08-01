FROM python:3.8-slim
#FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7
COPY . /app
WORKDIR /app
RUN pip install -r ./requirements.txt
EXPOSE 5000
CMD ["flask", "run", "--host",  "0.0.0.0"]
#EXPOSE 8000
#CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]