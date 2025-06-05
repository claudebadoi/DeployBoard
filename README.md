# 🚀 DeployBoard – Cloud-native Monitoring Dashboard

A simple yet powerful health check dashboard for monitoring websites and services. Built as a learning project for DevOps & Cloud Engineering.

![License](https://img.shields.io/badge/license-MIT-blue)  
![Status](https://img.shields.io/badge/status-in%20progress-yellow)  
![Last Commit](https://img.shields.io/github/last-commit/claudebadoi/DeployBoard)

---

## 📌 Overview

DeployBoard is a monitoring dashboard designed to check the health, uptime, and response time of various web services.

✅ Easy to configure  
✅ Dockerized + CI/CD via GitHub Actions  
✅ Deployed in the cloud (GCP / Railway / Vercel)  
✅ Real-time monitoring with auto-refresh (every 10 seconds)  
✅ Historical uptime charts for each monitored URL  
✅ Detailed logging of health checks  

---

## ⚙️ Tech Stack

- **Python** – scripting & backend logic  
- **Streamlit** – interactive dashboard with live graphs  
- **streamlit-autorefresh** – automatic periodic refresh of dashboard  
- **Docker** – containerized deployment  
- **GitHub Actions** – CI/CD automation  
- **Google Cloud Run / Railway** – cloud hosting  
- **Markdown + HTML** – status output

---

## 🛠️ Local Development Setup

```bash
# Clone repo
git clone https://github.com/claudebadoi/DeployBoard.git
cd DeployBoard

# Create virtual environment and install dependencies
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows
pip install -r requirements.txt

# Run dashboard locally
streamlit run dashboard.py

# Or using Docker
docker build -t deployboard .
docker run -p 8501:8501 deployboard
```

---

## 🎥 Demo & Screenshots

> 📹 [Click to watch Loom demo](https://loom.com/YOUR-VIDEO) *(coming soon)*

![Dashboard Preview](screenshots/preview.png)

---

## 🚧 Planned Features

- [x] Health check script with logging  
- [x] Real-time dashboard with auto-refresh every 10 seconds  
- [x] Historical status charts for monitored URLs  
- [x] Docker support for easy deployment  
- [ ] Notification system via email/Slack  
- [ ] Grafana integration (optional)  

---

## 📝 License

This project is licensed under the MIT License.
