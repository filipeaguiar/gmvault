import urllib.request
import json
import re

url = "https://raw.githubusercontent.com/5etools-mirror-3/5etools-src/master/data/items.json"
req = urllib.request.Request(url)
with urllib.request.urlopen(req) as response:
    data = json.loads(response.read().decode())

def get_pack_contents(pack_name, item_data):
    for item in item_data.get("item", []):
        if item.get("name") == pack_name:
            entries = json.dumps(item.get("entries", []))
            # find {@item name|source} or {@item name} or {@item name|source|display}
            # also wait, there might be quantities before the tag, like "10 {@item Torch|phb}"
            # Let's just find the items first
            matches = re.findall(r'\{@item ([^\|\}]+)(?:\|([^\|\}]+))?(?:\|([^\|\}]+))?\}', entries)
            return [m[0] for m in matches]
    return []

print(get_pack_contents("Burglar's Pack", data))
print(get_pack_contents("Dungeoneer's Pack", data))
