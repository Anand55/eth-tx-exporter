# Use official slim Python image
FROM python:3.11-slim

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir requests python-dotenv

ENV ETHERSCAN_API_KEY=your_key_here

CMD ["python", "src/main.py"]
