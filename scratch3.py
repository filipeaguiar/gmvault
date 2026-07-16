import urllib.request
import json
import re

url = "https://raw.githubusercontent.com/5etools-mirror-3/5etools-src/master/data/backgrounds.json"
req = urllib.request.Request(url)
with urllib.request.urlopen(req) as response:
    data = json.loads(response.read().decode())

def get_bg_equip(bg_name):
    for bg in data.get("background", []):
        if bg.get("name") == bg_name and bg.get("source") == "XPHB":
            equip = bg.get("startingEquipment", [])
            if equip and "A" in equip[0]:
                return equip[0]["A"]
    return []

print(get_bg_equip("Criminal"))
