import requests

def scan_url(target_url, word):
    """Escanea un sitio web buscando una palabra específica en las rutas."""
    full_url = f"{target_url.rstrip('/')}/{word}"

    try:
        response = requests.get(full_url, timeout=5)

        if response.status_code == 200:
            print(f"[+] Encontrado: {full_url} (Código 200)")
        elif response.status_code == 403:
            print(f"[-] Acceso denegado: {full_url} (Código 403)")
        elif response.status_code == 404:
            pass  # Silenciar si quieres ignorar los 404
        else:
            print(f"[?] Estado desconocido: {full_url} (Código {response.status_code})")

    except requests.exceptions.RequestException as e:
        print(f"[!] Error al conectar con {full_url}: {e}")

def busca_wd(target_url, wordlist_path):
    print(f"Buscando en: {target_url}\n")
    try:
        with open(wordlist_path, 'r', encoding='utf-8', errors='ignore') as archivo:
            for linea in archivo:
                palabra = linea.strip()
                if palabra:
                    scan_url(target_url, palabra)
    except FileNotFoundError:
        print(f"[!] El archivo '{wordlist_path}' no fue encontrado.")
    except Exception as e:
        print(f"[!] Error inesperado: {e}")

if __name__ == "__main__":
    TARGET_URL = "http://127.0.0.1:8000"
    WORDLIST_PATH = "common.txt"
    busca_wd(TARGET_URL, WORDLIST_PATH)
