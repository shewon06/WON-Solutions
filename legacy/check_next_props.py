import requests
import json
from bs4 import BeautifulSoup

url = "http://localhost:3000"
try:
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    next_data = soup.find('script', id='__NEXT_DATA__')
    if next_data:
        data = json.loads(next_data.string)
        is_connected = data.get('props', {}).get('pageProps', {}).get('isConnected')
        print(f"isConnected: {is_connected}")
    else:
        print("Could not find __NEXT_DATA__")
except Exception as e:
    print(f"Error: {e}")
