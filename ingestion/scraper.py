import requests
from bs4 import BeautifulSoup

URL = "https://www.tn.gov.in/schemes.php"

headers = {
    "User-Agent": "Mozilla/5.0"
}

response = requests.get(
    URL,
    headers=headers,
    timeout=30
)

response.raise_for_status()

soup = BeautifulSoup(response.text, "html.parser")

for link in soup.find_all("a", href=True):
    title = link.get_text(" ", strip=True)
    href = link["href"]

    if title:
        print(title, href)