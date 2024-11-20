import json
import requests

headers = { 
  "apikey": "3f9cf660-a63c-11ef-9831-479c9c8e62aa"}

params = (
   ("city","Batavia")
   ("state_name","Ohio"),
   ("country","us"),
);

response = requests.get('https://app.zipcodebase.com/api/v1/code/city', headers=headers, params=params);
print(response.text)