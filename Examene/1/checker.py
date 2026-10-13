import requests

# Listele menționate în cerință (exemplu pentru structură)
SECURITY_HEADERS = [
    "Content-Security-Policy",
    "Strict-Transport-Security",
    "X-Content-Type-Options",
    "X-Frame-Options"
]

SITES = [
    # Adresele standard pentru verificare
]

# --- Partea 1: Funcții ajutătoare ---

def build_url(host, path):
    """Construiește URL-ul complet, gestionând corect bara oblică (/)."""
    if not path.startswith("/"):
        path = "/" + path
    host = host.rstrip("/")
    return f"https://{host}{path}"

def is_https(url):
    """Verifică dacă URL-ul folosește protocolul HTTPS."""
    return url.startswith("https://")


# --- Partea 2: Trimiterea unei cereri ---

def show_response(url):
    """Trimite o cerere GET către URL și afișează codul de stare și Content-Type."""
    try:
        response = requests.get(url)
        print(f"Status: {response.status_code}")
        print(f"Content-Type: {response.headers.get('Content-Type')}")
    except requests.RequestException as e:
        print(f"Erore la efectuarea cererii: {e}")


# --- Exemple de testare ---
if __name__ == "__main__":
    # Test Partea 1
    print("--- Teste Partea 1 ---")
    print(build_url("example.com", "login"))   # https://example.com/login
    print(build_url("example.com", "/login"))  # https://example.com/login
    
    print(is_https("https://example.com"))     # True
    print(is_https("http://example.com"))      # False
    
    # Test Partea 2
    print("\n--- Teste Partea 2 ---")
    show_response("https://example.com")
    import requests

# Listele menționate în cerință
SECURITY_HEADERS = [
    "Content-Security-Policy",
    "Strict-Transport-Security",
    "X-Content-Type-Options",
    "X-Frame-Options"
]

SITES = [
    "https://httpbin.org/html",
    "https://httpbin.org/json",
    "https://example.com"
]

# --- Partea 1: Funcții ajutătoare ---

def build_url(host, path):
    """Construiește URL-ul complet, gestionând corect bara oblică (/)."""
    if not path.startswith("/"):
        path = "/" + path
    host = host.rstrip("/")
    return f"https://{host}{path}"

def is_https(url):
    """Verifică dacă URL-ul folosește protocolul HTTPS."""
    return url.startswith("https://")


# --- Partea 2: Trimiterea unei cereri ---

def show_response(url):
    """Trimite o cerere GET către URL și afișează codul de stare și Content-Type."""
    try:
        response = requests.get(url, timeout=5)
        print(f"Status: {response.status_code}")
        print(f"Content-Type: {response.headers.get('Content-Type')}")
    except requests.RequestException as e:
        print(f"Erore la efectuarea cererii: {e}")


# --- Partea 3: Un verificator reutilizabil ---

def check_site(url):
    """
    Verifică un site și returnează un dicționar cu detalii.
    Nu se oprește niciodată cu eroare (folosește try-except).
    """
    try:
        response = requests.get(url, timeout=5)
        
        # Extragem valoarea antetului 'Server', punând "unknown" dacă lipsește
        server_header = response.headers.get("Server", "unknown")
        
        return {
            "url": url,
            "status": response.status_code,
            "content_type": response.headers.get("Content-Type", "").split(";")[0],
            "length": len(response.content),
            "server": server_header
        }
    except requests.RequestException as e:
        return {
            "url": url,
            "status": None,
            "error": str(e)
        }


# --- Partea 4: Verificarea mai multor site-uri ---

def scan_sites():
    """
    Verifică fiecare site din SITES, filtrează pe cele cu status 200,
    le sortează după lungime (descrescător) și afișează un rezumat.
    """
    results = []
    success_count = 0
    fail_count = 0

    for site in SITES:
        result = check_site(site)
        if result.get("status") == 200:
            success_count += 1
            results.append(result)
        else:
            fail_count += 1

    # Sortează site-urile după length, cel mai mare primul
    results.sort(key=lambda x: x["length"], reverse=True)

    # Afișează rezultatele pentru site-urile care au mers
    for res in results:
        print(f"{res['url']} -> {res['status']}, {res['length']} octeți")

    print("\n--- Rezumat ---")
    print(f"Site-uri care au mers: {success_count}")
    print(f"Site-uri care au eșuat: {fail_count}")


# --- Execuție și Testare ---
if __name__ == "__main__":
    print("--- Test Partea 3 (check_site) ---")
    print(check_site("https://example.com"))
    
    print("\n--- Test Partea 4 (scan_sites) ---")
    scan_sites()
    #--- Partea 5:Audit de securitate----
    def check_headers(url):
    """
    Verifică prezența antetelor de securitate (SECURITY_HEADERS) într-un răspuns HTTP.
    Gestionează majusculele/minusculele, menține ordinea și calculează scorul procentual.
    """
    try:
        response = requests.get(url, timeout=5)
        headers = response.headers
        
        present = []
        missing = []
        
        for header in SECURITY_HEADERS:
            if header in headers:
                present.append(header)
            else:
                missing.append(header)
                
        total_headers = len(SECURITY_HEADERS)
        score = int((len(present) / total_headers) * 100) if total_headers > 0 else 0
        
        return {
            "present": present,
            "missing": missing,
            "score": score
        }
        
    except requests.RequestException as e:
        return {
            "status": None,
            "error": str(e)
        }
        # --- Partea 6: Încercări repetate ---

def retry_check(url, attempts=3):
    """Încearcă să trimită o cerere GET de cel mult 'attempts' ori în caz de eroare sau status >= 500."""
    last_status = None
    last_error = None
    
    for current_attempt in range(1, attempts + 1):
        try:
            response = requests.get(url, timeout=5)
            last_status = response.status_code
            
            # Dacă statusul este sub 500 (de exemplu 200, 404), ne oprim imediat
            if last_status < 500:
                return {
                    "status": last_status,
                    "attempts": current_attempt
                }
            # Dacă statusul este >= 500, bucla va continua până la 'attempts'
        except requests.RequestException as e:
            last_status = None
            last_error = str(e)
            # Eroarea de conexiune / timeout continuă următoarea încercare
            
    # Dacă s-au epuizat încercările
    result = {
        "status": last_status,
        "attempts": attempts
    }
    if last_error:
        result["error"] = last_error
        
    return result
    
