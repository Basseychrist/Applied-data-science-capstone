import requests
from bs4 import BeautifulSoup

static_url = "https://en.wikipedia.org/w/index.php?title=List_of_Falcon_9_and_Falcon_Heavy_launches&oldid=1027686922"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/91.0.4472.124 Safari/537.36"
}
response = requests.get(static_url, headers=headers)
print(f"Status Code: {response.status_code}")
soup = BeautifulSoup(response.text, 'html.parser')
print(f"Title: {soup.title}")
