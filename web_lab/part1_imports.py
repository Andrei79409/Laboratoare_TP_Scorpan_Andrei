# Laborator: functii, metode si importuri pe web
# Student: Andrei Scorpan

import time
import requests
import urllib.request

BASE_URL = "https://cybercor.org"
ECHO_URL = "https://httpbin.org"
TIMEOUT = 10  # secunde

# Exercitiul 1
print("Ex 1 - Versiune requests:", requests.__version__)
# requests a avut nevoie de pip install deoarece este o biblioteca externa (third-party).
# urllib nu necesita instalare pentru ca vine deja inclus in biblioteca standard Python.

# Exercitiul 2
response_ex2 = requests.get(BASE_URL, timeout=TIMEOUT)
print("Ex 2 - Cod stare (import normal):", response_ex2.status_code)

from requests import get
response_ex2_from = get(BASE_URL, timeout=TIMEOUT)
# Avantaj 'import requests': Spatiul de nume e clar, stim exact carei biblioteci apartine functia apelata.
# Avantaj 'from requests import get': Codul devine mai scurt si mai rapid de scris.

# Exercitiul 3
import requests as rq
response_ex3 = rq.get(BASE_URL, timeout=TIMEOUT)
# Un alias (precum pd pentru pandas sau rq pentru requests) face codul mai usor de citit cand numele modulului este prea lung.
# il face mai greu de citit daca folosim un alias nestandard care confuzeaza alti programatori.

# Exercitiul 4
response_ex4 = urllib.request.urlopen(BASE_URL)
print("Ex 4 - Status urllib:", response_ex4.status)
print("Ex 4 - Corp:", response_ex4.read()[:200].decode("utf-8"))

# Exercitiul 5
# print(dir(requests))
# 1. get -> este o functie
# 2. Session -> este o clasa
# 3. exceptions -> este un modul

# Exercitiul 6
# Ruland help(requests.get) aflam ca parametrul se numeste 'timeout'.
response_ex6 = requests.get(BASE_URL, timeout=TIMEOUT)

# Exercitiul 7
t_start = time.perf_counter()
response_ex7 = requests.get(BASE_URL, timeout=TIMEOUT)
t_stop = time.perf_counter()
print("Ex 7 - Timp perf_counter:", t_stop - t_start)
print("Ex 7 - Timp response.elapsed:", response_ex7.elapsed.total_seconds())

# Exercitiul 8
try:
    import bs4
except ImportError:
    print("Instalati modulul cu: pip install beautifulsoup4")