import urllib.request
import json
import re

url = "https://raw.githubusercontent.com/5etools-mirror-3/5etools-src/master/data/class/class-rogue.json"
req = urllib.request.Request(url)
with urllib.request.urlopen(req) as response:
    data = json.loads(response.read().decode())

rogue = next((c for c in data["class"] if c["source"] == "XPHB"), None)
if rogue:
    equip = rogue.get("startingEquipment", {})
    print(json.dumps(equip, indent=2))
