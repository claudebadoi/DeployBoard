# --- Importuri externe ---
import requests
import streamlit as st
import pandas as pd
import threading
import logging
import sys
from prometheus_client import start_http_server, Gauge
from streamlit_autorefresh import st_autorefresh

# =======================
# Configurari initiale
# =======================

# Setam configurarea aplicatiei (nume, layout etc.)
st.set_page_config(page_title="DeployBoard – URL Status Monitor", layout="wide")

# Logging basic pentru terminal
logger = logging.getLogger()
if not logger.hasHandlers():
    logger.setLevel(logging.INFO)
    handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter('%(asctime)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

# Pornim serverul Prometheus (doar o data)
if "prometheus_started" not in st.session_state:
    def start_metrics_server():
        start_http_server(8000)  # ruleaza pe portul 8000


    threading.Thread(target=start_metrics_server, daemon=True).start()
    st.session_state.prometheus_started = True

# Creare metric pentru status URL (1 = UP, 0 = DOWN)
if "url_status_gauge" not in st.session_state:
    try:
        st.session_state.url_status_gauge = Gauge(
            'url_status',
            'Status of the URL (1=UP, 0=DOWN)',
            ['url']
        )
    except ValueError:
        # In caz ca a fost deja inregistrat
        st.session_state.url_status_gauge = None


# =======================
# Functii helper
# =======================

def check_health(url):
    """Verifica daca un URL este UP sau DOWN"""
    try:
        response = requests.get(url, timeout=5)
        status = 1 if response.status_code == 200 else 0
        logger.info(f"{url} este {'UP' if status else 'DOWN'}")
    except requests.RequestException as e:
        status = 0
        logger.error(f"{url} este DOWN – Eroare: {e}")

    # Update metric Prometheus daca exista
    if st.session_state.url_status_gauge:
        st.session_state.url_status_gauge.labels(url=url).set(status)

    return status


def render_status(status):
    """Returneaza emoji, culoare si text pentru status"""
    return ("✅", "green", "UP") if status == 1 else ("❌", "red", "DOWN")


# =======================
# Aplicatia principala
# =======================

def main():
    st.title("🌐 DeployBoard – Monitorizare Status URL")
    st.markdown("Adauga oricate URL-uri doresti mai jos.")

    # Auto-refresh la fiecare 10 secunde
    st_autorefresh(interval=10 * 1000, key="auto_refresh")

    # Initializare sesiuni
    if "urls" not in st.session_state:
        st.session_state.urls = [
            "https://github.com",
            "https://google.com",
            "https://httpbin.io/unstable?failure_rate=0.5"
        ]

    if "history" not in st.session_state:
        st.session_state.history = {}

    # === Form pentru adaugarea unui nou URL ===
    with st.form("add_url_form", clear_on_submit=True):
        new_url = st.text_input("🔗 Introdu un nou URL de monitorizat")
        submitted = st.form_submit_button("➕ Adauga URL")
        if submitted and new_url:
            if new_url not in st.session_state.urls:
                st.session_state.urls.append(new_url)
                st.success(f"Adaugat: {new_url}")
            else:
                st.warning("URL-ul este deja in lista.")

    # Buton de refresh manual
    if st.button("🔄 Refresh acum"):
        st.session_state['force_rerun'] = st.session_state.get('force_rerun', 0) + 1

    # Verifica statusul fiecarui URL
    current_statuses = {}
    for url in st.session_state.urls:
        status = check_health(url)

        if url not in st.session_state.history:
            st.session_state.history[url] = []

        st.session_state.history[url].append(status)
        st.session_state.history[url] = st.session_state.history[url][-20:]  # ultimile 20 statusuri

        current_statuses[url] = status

    # Pregatim datele pentru tabel
    table_data = []
    for url in st.session_state.urls:
        status = current_statuses[url]
        emoji, color, text = render_status(status)
        history = st.session_state.history[url][-10:]
        history_emojis = "".join("✅" if s == 1 else "❌" for s in history)
        up_count = st.session_state.history[url].count(1)
        total_checks = len(st.session_state.history[url])
        uptime_pct = (up_count / total_checks) * 100 if total_checks > 0 else 0

        table_data.append({
            "URL": url,
            "Status": f"<span style='color:{color}; font-size:20px;'>{emoji} {text}</span>",
            "Istoric (ultimele 10)": history_emojis,
            "Uptime %": f"{uptime_pct:.1f}%",
            "Total verificari": total_checks
        })

    df = pd.DataFrame(table_data)

    # Stilizare tabel
    st.markdown("""
        <style>
        table { width: 100%; border-collapse: collapse; }
        th, td { border: 1px solid #ddd; padding: 8px; text-align: center; }
        th { background-color: #4CAF50; color: white; }
        </style>
    """, unsafe_allow_html=True)

    # Afisam tabelul folosind HTML personalizat
    table_html = "<table><thead><tr>"
    for col in df.columns:
        table_html += f"<th>{col}</th>"
    table_html += "</tr></thead><tbody>"
    for _, row in df.iterrows():
        table_html += "<tr>"
        for col in df.columns:
            table_html += f"<td>{row[col]}</td>"
        table_html += "</tr>"
    table_html += "</tbody></table>"

    st.markdown(table_html, unsafe_allow_html=True)


# =======================
# Punct de intrare
# =======================
if __name__ == "__main__":
    main()
