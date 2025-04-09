# server/Dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY server.py .

RUN pip install flask

EXPOSE 5050

CMD ["python", "server.py"]
