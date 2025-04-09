FROM python:3.10-slim

WORKDIR /app

COPY node.py .

RUN pip install requests
RUN apt update && apt install -y curl

CMD ["python", "node.py"]
