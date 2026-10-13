# Laborator: funcții, metode și importuri pe web
# Student: Andrei Scorpan

import requests
import time
import urllib.parse
import re
import socket
import ssl
import json
from html.parser import HTMLParser

DEFAULT_HEADERS = {"User-Agent": "WebLab-Andrei"}

def fetch(url, timeout=10):
    return requests.get(url, headers=DEFAULT_HEADERS, timeout=timeout)

def get_status(url):
    return fetch(url).status_code

def get_title(html):
    start = html.find("<title>") + len("<title>")
    end = html.find("</title>")
    if start != -1 and end != -1:
        return html[start:end].strip()
    return "N/A"

def security_headers(url):
    h = fetch(url).headers
    return {
        "Strict-Transport-Security": "Strict-Transport-Security" in h,
        "Content-Security-Policy": "Content-Security-Policy" in h,
        "X-Frame-Options": "X-Frame-Options" in h,
        "X-Content-Type-Options": "X-Content-Type-Options" in h,
        "Referrer-Policy": "Referrer-Policy" in h
    }

def score_headers(results):
    return f"{sum(1 for v in results.values() if v)}/{len(results)}"

def extract_links(html):
    return list(set(re.findall(r'href="([^"]+)"', html)))

def split_links(links, domain):
    interne, externe = [], []
    for link in links:
        full_url = urllib.parse.urljoin(f"https://{domain}", link)
        if urllib.parse.urlparse(full_url).netloc == domain:
            interne.append(full_url)
        else:
            externe.append(full_url)
    return interne, externe

def fetch_robots(base):
    try:
        r = fetch(base + "/robots.txt")
        r.raise_for_status()
        return r.text
    except requests.RequestException:
        return None

def disallowed_paths(robots_text):
    if not robots_text: return []
    return [lin.split(":", 1)[1].strip() for lin in robots_text.splitlines() if lin.lower().startswith("disallow:")]

def resolve(hostname):
    return socket.gethostbyname(hostname)

def cert_days_left(hostname):
    ctx = ssl.create_default_context()
    with socket.create_connection((hostname, 443)) as sock:
        with ctx.wrap_socket(sock, server_hostname=hostname) as ssock:
            cert = ssock.getpeercert()
            not_after = ssl.cert_time_to_seconds(cert["notAfter"])
            return int((not_after - time.time()) / 86400)

def site_report(url):
    print(f"=== Raport site: {url} ===")
    domain = urllib.parse.urlparse(url).netloc
    
    res = fetch(url)
    print(f"Cod de stare:      {res.status_code}")
    print(f"Titlu:             {get_title(res.text)}")
    print(f"Adresă IP:         {resolve(domain)}")
    
    http_url = url.replace("https://", "http://")
    res_http = fetch(http_url)
    redirs = [f"{r.status_code} ->" for r in res_http.history] + [res_http.url]
    print(f"Redirecționări:    {' '.join(redirs)}")
    
    sh = security_headers(url)
    print(f"Scor securitate:   {score_headers(sh)}")
    print(f"Certificat:        {cert_days_left(domain)} de zile rămase")
    
    links = extract_links(res.text)
    interne, externe = split_links(links, domain)
    print(f"Legături:          {len(interne)} interne, {len(externe)} externe")
    
    robots = fetch_robots(url)
    disallowed = disallowed_paths(robots)
    print(f"Căi interzise:     {', '.join(disallowed)}")

    raport_json = {
        "status": res.status_code,
        "titlu": get_title(res.text),
        "ip": resolve(domain),
        "scor_securitate": score_headers(sh),
        "certificat_zile": cert_days_left(domain),
        "legaturi_interne": len(interne),
        "legaturi_externe": len(externe),
        "cai_interzise": disallowed
    }
    with open("report.json", "w") as f:
        json.dump(raport_json, f, indent=2)
    print("Salvat în report.json")

if __name__ == "__main__":
    # Autotestul rulează doar dacă fișierul este executat direct.
    # Dacă este importat în main.py, variabila __name__ va fi 'webtools', deci condiția pică și codul nu rulează de 2 ori.
    print("Autotest:", get_status("https://cybercor.org"))