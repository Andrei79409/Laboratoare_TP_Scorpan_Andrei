# Laborator: funcții, metode și importuri pe web
# Student: Andrei Scorpan

import time
import requests

BASE_URL = "https://cybercor.org"
TIMEOUT = 10

# Exercițiul 21 & 23
def fetch(url, timeout=10):
    """Returnează obiectul răspuns pentru adresa url."""
    return requests.get(url, timeout=timeout)

print("Ex 21 status:", fetch(BASE_URL).status_code)
time.sleep(1)

# Exercițiul 22
def get_status(url: str) -> int:
    """Returnează codul de stare HTTP pentru adresa url."""
    return fetch(url, timeout=TIMEOUT).status_code

for cale in ["/", "/robots.txt", "/sitemap.xml"]:
    print(f"Status pt {cale}:", get_status(BASE_URL + cale))
    time.sleep(1)

# Exercițiul 24, 25 & 26
def get_title(html: str) -> str:
    """Extrage și returnează titlul paginii dintr-un cod HTML."""
    start = html.find("<title>") + len("<title>")
    end = html.find("</title>")
    if start != -1 and end != -1:
        return html[start:end].strip()
    return "Fără titlu"

# print(help(get_title))
# La apelul get_status(123), Python nu oprește automat programul, 
# deoarece adnotările de tip (type hints) sunt ignorate la runtime, fiind doar sugestii pentru lintere.

# Exercițiul 27
def page_exists(url):
    try:
        requests.get(url, timeout=TIMEOUT)
        return True
    except requests.RequestException:
        return False

# Exercițiul 28
def check_paths(base, paths):
    rezultat = {}
    for p in paths:
        rezultat[p] = get_status(base + p)
        time.sleep(1)
    return rezultat

# Exercițiul 29
def get_header(url, name, default="lipsește"):
    res = fetch(url)
    return res.headers.get(name, default)

print("Server Header:", get_header(BASE_URL, name="Server"))

# Exercițiul 30
def security_headers(url):
    h = fetch(url).headers
    return {
        "Strict-Transport-Security": "Strict-Transport-Security" in h,
        "Content-Security-Policy": "Content-Security-Policy" in h,
        "X-Frame-Options": "X-Frame-Options" in h,
        "X-Content-Type-Options": "X-Content-Type-Options" in h,
        "Referrer-Policy": "Referrer-Policy" in h
    }

# Exercițiul 31
def score_headers(results):
    scor = sum(1 for v in results.values() if v)
    return f"{scor}/{len(results)}"

print("Scor securitate:", score_headers(security_headers(BASE_URL)))

# Exercițiul 32
def fetch_robots(base):
    try:
        r = requests.get(base + "/robots.txt", timeout=TIMEOUT)
        r.raise_for_status()
        return r.text
    except requests.RequestException:
        return None

def disallowed_paths(robots_text):
    if not robots_text:
        return []
    cai = []
    for linie in robots_text.splitlines():
        if linie.lower().startswith("disallow:"):
            cai.append(linie.split(":", 1)[1].strip())
    return cai

# Exercițiul 33
def response_times(*urls):
    rezultat = {}
    for url in urls:
        r = fetch(url)
        rezultat[url] = r.elapsed.total_seconds()
        time.sleep(1)
    return rezultat

# Exercițiul 34
def log(message, **details):
    detalii_str = " | ".join(f"{k}={v}" for k, v in details.items())
    print(f"{message} | {detalii_str}")

log("verificat", url=BASE_URL, status=200)