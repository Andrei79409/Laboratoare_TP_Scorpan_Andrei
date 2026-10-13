# Laborator: funcții, metode și importuri pe web
# Student: Andrei Scorpan

import argparse
import csv
from datetime import datetime
import time

import webtools
from webtools import DEFAULT_HEADERS
# Dacă main.py ar avea propria sa funcție get_title, importând 'from webtools import get_title', 
# am suprascrie funcția locală cu cea din webtools (sau invers, în funcție de ordine).

def check_paths_local(base, paths):
    rezultat = {}
    for p in paths:
        rezultat[p] = webtools.get_status(base + p)
        time.sleep(1)
    return rezultat

def main():
    parser = argparse.ArgumentParser(description="Generează raport site")
    parser.add_argument("url", help="URL-ul de verificat")
    args = parser.parse_args()

    print("Se folosesc headerele:", DEFAULT_HEADERS)

    # Exercițiul 49: Creare raport CSV
    paths_to_check = ["/", "/robots.txt", "/sitemap.xml"]
    results = check_paths_local(args.url, paths_to_check)
    
    with open("report.csv", "w", newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["path", "status", "checked_at"])
        for p, s in results.items():
            writer.writerow([p, s, datetime.now().isoformat()])

    # Apelul final pentru raport
    webtools.site_report(args.url)

if __name__ == "__main__":
    main()