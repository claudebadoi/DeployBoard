import requests  # library for checking https


# functia pentru verificarea URL
def check_health(url):
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            print(f"{url} este UP ✅")
        else:
            print(f"{url} a răspuns cu codul: {response.status_code} ⚠️")
    except requests.RequestException as e:
        print(f"{url} este DOWN ❌ – Eroare: {e}")


if __name__ == "__main__":
    urls = [
        "https://github.com",
        "https://google.com",
        "https://thisdomaindoesnotexist.tld"
          ]

    for url in urls:
        check_health(url)
