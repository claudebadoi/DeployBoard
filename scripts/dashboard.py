import requests
import streamlit as st
import logging
import sys
import pandas as pd
from streamlit_autorefresh import st_autorefresh
from prometheus_client import start_http_server, Gauge
import threading

# === Pornire server Prometheus ===
if "prometheus_started" not in st.session_state:
    def start_metrics_server():
        start_http_server(8000)
    threading.Thread(target=start_metrics_server, daemon=True).start()
    st.session_state.prometheus_started = True

# === Inițializare Gauge pentru URL status ===
if "url_status_gauge" not in st.session_state:
    st.session_state.url_status_gauge = Gauge('url_status', 'Status of the URL (1=UP, 0=DOWN)', ['url'])

url_status = st.session_state.url_status_gauge

# === Configurare logging (doar în consolă) ===
logger = logging.getLogger()
if not logger.hasHandlers():
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(message)s')
    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

# === Funcție de verificare a stării URL-urilor ===
def check_health(url):
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            status = 1
            logger.info(f"{url} este UP")
        else:
            status = 0
            logger.warning(f"{url} a răspuns cu codul: {response.status_code}")
    except requests.RequestException as e:
        status = 0
        logger.error(f"{url} este DOWN – Eroare: {e}")
    url_status.labels(url=url).set(status)
    return status

# === UI principal ===
def main():
    st.title("🌐 DeployBoard – Status URL")
    st.write("Verifică starea serviciilor online (actualizare automată la fiecare 10 secunde)")

    st_autorefresh(interval=10 * 1000, key="refresh")

    urls = [
        "https://github.com",
        "https://google.com",
        "https://thisdomaindoesnotexist.tld"
    ]

    if "history" not in st.session_state:
        st.session_state.history = {url: [] for url in urls}

    for url in urls:
        status = check_health(url)
        st.session_state.history[url].append(status)

    cols = st.columns(len(urls))
    for idx, url in enumerate(urls):
        status_list = st.session_state.history[url]
        if status_list:
            df = pd.DataFrame(status_list, columns=["Status"])
            cols[idx].write(f"Status istoric pentru: **{url}**")
            cols[idx].bar_chart(df)

# === Punctul de intrare ===
if __name__ == "__main__":
    if "--test" in sys.argv:
        urls = [
            "https://github.com",
            "https://google.com",
            "https://thisdomaindoesnotexist.tld"
        ]
        for url in urls:
            status = check_health(url)
            print(f"{url}: {'UP' if status == 1 else 'DOWN'}")
    else:
        main()
