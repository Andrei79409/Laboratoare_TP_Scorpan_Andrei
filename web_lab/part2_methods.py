# Laborator: funcții, metode și importuri pe web
# Student: Andrei Scorpan

import time
import requests

BASE_URL = "https://cybercor.org"
ECHO_URL = "https://httpbin.org"
TIMEOUT = 10

response = requests.get(BASE_URL, timeout=TIMEOUT)
time.sleep(1)

# Exercițiul 9
print("Status:", response.status_code) # atribut
print("Ok:", response.ok)              # atribut
print("URL:", response.url)            # atribut
print("Encoding:", response.encoding)  # atribut

# Exercițiul 10
response.raise_for_status()
try:
    bad_resp = requests.get(BASE_URL + "/this-page-does-not-exist", timeout=TIMEOUT)
    bad_resp.raise_for_status()
except requests.HTTPError:
    print("Pagina căutată nu a fost găsită (404). Ne cerem scuze!")
time.sleep(1)

# Exercițiul 11
for nume, valoare in response.headers.items():
    print(f"{nume}: {valoare}")

# Exercițiul 12
print("Server:", response.headers.get("Server", "lipsește"))
print("Content-Type:", response.headers.get("Content-Type", "lipsește"))
print("content-type (litere mici):", response.headers.get("content-type", "lipsește"))
# Se observă că dicționarul de headere din requests este case-insensitive (nu ține cont de litere mari/mici).

# Exercițiul 13
print("Apariții cyber:", response.text.lower().count("cyber"))
# Putem înlănțui .lower() și .count() deoarece .lower() returnează un șir de caractere (string), iar clasa string are metoda .count().

# Exercițiul 14
html = response.text
start = html.find("<title>") + len("<title>")
end = html.find("</title>")
titlu = html[start:end].strip()
print("Titlu pagină:", titlu)

# Exercițiul 15
lines = html.splitlines()
print("Număr linii:", len(lines))
cea_mai_lunga = max(lines, key=len)
print("Lungimea celei mai lungi linii:", len(cea_mai_lunga))

# Exercițiul 16
if response.url.startswith("https://"):
    print("Conexiune securizată")
else:
    print("Conexiune nesecurizată")

# Exercițiul 17
res_http = requests.get("http://cybercor.org", timeout=TIMEOUT)
for r in res_http.history:
    print(f"Redirecționare: {r.status_code} -> {r.url}")
print("URL final:", res_http.url)
time.sleep(1)

# Exercițiul 18
res_head = requests.head(BASE_URL, timeout=TIMEOUT)
res_get = requests.get(BASE_URL, timeout=TIMEOUT)
print("Lungime HEAD:", len(res_head.content))
print("Lungime GET:", len(res_get.content))
# Diferența e că cererea HEAD aduce doar antetele (headers), fără corpul propriu-zis (body), deci content-ul este gol.

# Exercițiul 19
if len(response.cookies) == 0:
    print("Niciun cookie setat")
else:
    for cookie in response.cookies:
        print(f"Cookie: {cookie.name}, Secure: {cookie.secure}")

# Exercițiul 20
session = requests.Session()
session.headers.update({"User-Agent": "WebLab-Andrei"})
res_echo = session.get(ECHO_URL + "/headers", timeout=TIMEOUT)
print("Răspuns antete:\n", res_echo.text)