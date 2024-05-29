import os
import requests

def fetch_data():
    url = "https://api.example.com"
    username = os.environ.get("API_USERNAME")
    password = os.environ.get("API_PASSWORD")

    if not (username and password):
        raise ValueError("API credentials not found in environment variables.")

    response = requests.get(url, auth=(username, password))
    return response.json()

