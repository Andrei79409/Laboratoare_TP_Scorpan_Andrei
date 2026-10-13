from checker import (
    build_url, 
    is_https, 
    show_response, 
    check_site, 
    scan_sites, 
    check_headers, 
    retry_check
)

print("=== PARTEA 1: Funcții ajutătoare ===")
print("1. build_url (fără bară):", build_url("example.com", "login"))
print("1. build_url (cu bară):", build_url("example.com", "/login"))
print("2. is_https (HTTPS valid):", is_https("https://example.com"))
print("2. is_https (HTTP invalid):", is_https("http://example.com"))

print("\n=== PARTEA 2: Trimiterea unei cereri ===")
print("show_response pentru https://example.com:")
show_response("https://example.com")

print("\n=== PARTEA 3: Un verificator reutilizabil ===")
print("check_site (site valid):", check_site("https://example.com"))
print("check_site (site invalid):", check_site("http://site-inexistent-12345.invalid"))

print("\n=== PARTEA 4: Verificarea mai multor site-uri ===")
print("Rezultate scan_sites():")
scan_sites()

print("\n=== PARTEA 5: Audit de securitate ===")
print("check_headers pentru https://example.com:", check_headers("https://example.com"))
print("check_headers pentru site invalid:", check_headers("http://site-inexistent-12345.invalid"))

print("\n=== PARTEA 6: Încercări repetate ===")
print("retry_check (status 200):", retry_check("https://httpbin.org/status/200"))
print("retry_check (status 404 - oprire imediată):", retry_check("https://httpbin.org/status/404"))
print("retry_check (status 500 - 3 încercări):", retry_check("https://httpbin.org/status/500"))
print("retry_check (adresă inexistentă):", retry_check("http://site-inexistent-12345.invalid"))
