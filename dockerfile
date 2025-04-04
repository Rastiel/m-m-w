FROM python:3.11-slim

WORKDIR /app
ENV PYTHONUNBUFFERED=TRUE

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

CMD ["gunicorn", "--bind", "0.0.0.0:10000", "--log-syslog", "True", "--capture-output", "--access-logfile", "-", "app:app"]
