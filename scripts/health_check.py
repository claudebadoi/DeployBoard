import requests  #library for checking https
import logging
import sys

from datetime import datetime

#functia pentru loggin in fisierul health_check.log
logger = logging.getLogger()
logger.setLevel(logging.INFO)

#pentru afisare log in terminalul docker si fisierul log
formatter = logging.Formatter('%(asctime)s - %(message)s')
stream_handler = logging.StreamHandler(sys.stdout)

file_handler = logging.FileHandler('health_check.log')
file_handler.setFormatter(formatter)

logger.addHandler(stream_handler)
logger.addHandler(file_handler)

#functia pentru verificarea URL
def check_health(url):
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            logging.info(f"{url} este UP")
        else:
            logging.warning(f"{url} a raspuns cu codul: {response.status_code}")
    except requests.RequestException as e:
        logging.error(f"{url} este DOWN – Eroare: {e}")


if __name__ == "__main__":
    urls = [
        "https://github.com",
        "https://google.com",
        "https://thisdomaindoesnotexist.tld"
          ]

    for url in urls:
        check_health(url)
