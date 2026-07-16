import urllib.request
import json
import re

url = "https://raw.githubusercontent.com/5etools-mirror-3/5etools-src/master/data/class/index.json"
req = urllib.request.Request(url)
with urllib.request.urlopen(req) as response:
    index = json.loads(response.read().decode())

for k, filename in index.items():
    if k in ["fighter", "cleric", "wizard", "rogue"]:
        url2 = "https://raw.githubusercontent.com/5etools-mirror-3/5etools-src/master/data/class/" + filename
        req2 = urllib.request.Request(url2)
        with urllib.request.urlopen(req2) as res2:
            data = json.loads(res2.read().decode())
        cls = next((c for c in data["class"] if c["source"] == "XPHB"), None)
        if cls:
            equip = cls.get("startingEquipment", {})
            print(k, ":")
            print(equip.get("defaultData", [{}])[0].get("A", []))
