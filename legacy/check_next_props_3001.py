import urllib.request
import json
import re

url = "http://localhost:3001"
try:
    with urllib.request.urlopen(url) as response:
        html = response.read().decode('utf-8')
        match = re.search(r'<script id="__NEXT_DATA__" type="application/json">(.*?)</script>', html, re.DOTALL)
        if match:
            data = json.loads(match.group(1))
            is_connected = data.get('props', {}).get('pageProps', {}).get('isConnected')
            print(f"isConnected: {is_connected}")
        else:
            print("Could not find __NEXT_DATA__")
except Exception as e:
    print(f"Error: {e}")
