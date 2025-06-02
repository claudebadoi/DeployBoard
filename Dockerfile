
FROM python:3.11-slim

WORKDIR /app

COPY scripts/health_check.py .


RUN pip install requests

CMD ["python", "health_check.py"]
