FROM python:3.8.5-slim

WORKDIR /app

RUN pip install discord PyNaCl

COPY bot.py bot.py

CMD ["python3", "bot.py"]
