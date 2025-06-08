# Folosește imagine oficială Python 3.11 slim ca bază
FROM python:3.11-slim

# Setează directorul de lucru în container
WORKDIR /app

# Copiază fișierele de requirements și aplicația
COPY requirements.txt .
COPY dashboard.py .

# Instalează dependențele
RUN pip install --no-cache-dir -r requirements.txt

# Expune porturile necesare
EXPOSE 8501   # Streamlit
EXPOSE 8000   # Prometheus metrics

# Rulează aplicația Streamlit pe toate interfețele la portul 8501
CMD ["streamlit", "run", "dashboard.py", "--server.port=8501", "--server.address=0.0.0.0"]
