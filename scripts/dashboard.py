import requests
import streamlit as st
import logging
import sys
import pandas as pd
from streamlit_autorefresh import st_autorefresh

# Logging setup
logger = logging.getLogger()
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(message)s')
stream_handler = logging.StreamHandler(sys.stdout)
file_handler = logging.FileHandler('health_check.log')
file_handler.setFormatter(formatter)
logger.addHandler(stream_handler)
logger.addHandler(file_handler)

def check_health(url):
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            status = 1  # UP
            logger.info(f"{url} este UP")
        else:
            status = 0  # DOWN
            logger.warning(f"{url} a raspuns cu codul: {response.status_code}")
    except requests.RequestException as e:
        status = 0  # DOWN
        logger.error(f"{url} este DOWN – Eroare: {e}")
    return status

def main():
    st.title("🌐 DeployBoard – Status URL")
    st.write("Verifică starea serviciilor online (actualizare automată la fiecare 10 secunde)")

    # Refresh automat la fiecare 10 secunde
    st_autorefresh(interval=10 * 1000, key="refresh")

    urls = [
        "https://github.com",
        "https://google.com",
        "https://thisdomaindoesnotexist.tld"
    ]

    # Inițializare istoric in session_state
    if "history" not in st.session_state:
        st.session_state.history = {url: [] for url in urls}

    # Verificăm starea URL-urilor și stocăm rezultatele
    for url in urls:
        status = check_health(url)
        st.session_state.history[url].append(status)

    # Aranjare coloane pentru grafice
    cols = st.columns(len(urls))

    for idx, url in enumerate(urls):
        status_list = st.session_state.history[url]
        if status_list:
            df = pd.DataFrame(status_list, columns=["Status"])
            cols[idx].write(f"Status istoric pentru: **{url}**")
            cols[idx].bar_chart(df)

if __name__ == "__main__":
    main()
