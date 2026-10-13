# Laborator: funcții, metode și importuri pe web
# Student: Andrei Scorpan

import urllib.parse
import re
from html.parser import HTMLParser
import hashlib
import json
import socket
import ssl
import datetime
import requests
import time

BASE_URL = "https://cybercor.org"
TIMEOUT = 10

# Exercițiul 35
parsed_url = urllib.parse.urlparse("https://cybercor.org/path?x=1#top")
print("Scheme:", parsed_url.scheme)
print("Netloc:", parsed_url.netloc)
print("Path:", parsed_url.path)
print("Query:", parsed_url.query)
print("Fragment:", parsed_url.fragment)

# Exercițiul 36
print(urllib.parse.urljoin(BASE_URL, "/about"))
print(urllib.parse.urljoin(BASE_URL, "contact.html"))
print(urllib.parse.urljoin(BASE_URL, "../index.html"))

# Exercițiul 37
def extract_links(html):
    return list(set(re.findall(r'href="([^"]+)"', html)))

# Exercițiul 38
def split_links(links, domain):
    interne = []
    externe = []
    for link in links:
        full_url = urllib.parse.urljoin(f"https://{domain}", link)
        link_domain = urllib.parse.urlparse(full_url).netloc
        if link_domain == domain:
            interne.append(full_url)
        else:
            externe.append(full_url)
    return interne, externe

# Exercițiul 39
class ImageFinder(HTMLParser):
    def __init__(self):
        super().__init__()
        self.images = []

    def handle_starttag(self, tag, attrs):
        if tag.lower() == "img":
            src = dict(attrs).get("src")
            if src:
                self.images.append(src)

test_html = """
<html><body>
  <img src="/logo.png" alt="Logo">
  <IMG SRC="poza.jpg">
  <img alt="imagine fără src">
  <img src="https://cdn.example.com/banner.webp" />
  <a href="/despre">Aceasta nu este o imagine</a>
</body></html>
"""
finder = ImageFinder()
finder.feed(test_html)
assert finder.images == [
    "/logo.png",
    "poza.jpg",
    "https://cdn.example.com/banner.webp",
], "Parserul nu a găsit exact imaginile așteptate"
print("Testul pentru parser a trecut!")

# Exercițiul 40
def page_fingerprint(url):
    res = requests.get(url, timeout=TIMEOUT)
    return hashlib.sha256(res.content).hexdigest()

# Exercițiul 41
res_headers = requests.get(BASE_URL, timeout=TIMEOUT).headers
with open("headers.json", "w") as file:
    json.dump(dict(res_headers), file, indent=2)

with open("headers.json", "r") as file:
    date_incarcate = json.load(file)
    print("Antet încărcat (Server):", date_incarcate.get("Server"))

# Exercițiul 42
def resolve(hostname):
    return socket.gethostbyname(hostname)
print("IP Cybercor:", resolve("cybercor.org"))

# Exercițiul 43
def cert_days_left(hostname):
    context = ssl.create_default_context()
    with socket.create_connection((hostname, 443)) as sock:
        with context.wrap_socket(sock, server_hostname=hostname) as ssock:
            cert = ssock.getpeercert()
            not_after = ssl.cert_time_to_seconds(cert["notAfter"])
            zile_ramase = (not_after - time.time()) / (24 * 3600)
            return int(zile_ramase)

print("Zile certificat rămase:", cert_days_left("cybercor.org"))