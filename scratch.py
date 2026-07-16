import urllib.request
import json
DATA_BASE_URL = "https://raw.githubusercontent.com/5etools-mirror-3/5etools-src/master/data/"

def load_from_5etools(filename):
    headers = {'User-Agent': 'Mozilla/5.0'}
    url = DATA_BASE_URL + filename
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req) as response:
            return json.loads(response.read().decode())
    except Exception as e:
        print(f"  [5e.tools] Erro ao carregar {filename}: {e}")
        return None
