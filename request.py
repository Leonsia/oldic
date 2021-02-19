import requests

url = 'http://localhost:5000/lookup'
r = requests.post(url, json={'word': 5})
#print(r.json())
