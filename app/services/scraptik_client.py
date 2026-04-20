import requests
from app.config import RAPIDAPI_KEY

API_HOST = "tiktok-api23.p.rapidapi.com"


class ScrapTikError(Exception):
    pass


def fetch_user(username: str) -> dict:
    url = "https://tiktok-api23.p.rapidapi.com/api/user/info"

    querystring = {"uniqueId": username}

    headers = {
        "x-rapidapi-key": RAPIDAPI_KEY,
        "x-rapidapi-host": API_HOST
    }

    response = requests.get(url, headers=headers, params=querystring)

    if response.status_code != 200:
        raise ScrapTikError(f"API Fehler: {response.status_code}")

    data = response.json()

    if not data:
        raise ScrapTikError("Keine Daten erhalten")

    return data