import requests
import json
post = {
    "username": "jose@doe.com",
    "password": "password"
}
print(json.dumps(post))
data = {'input': 'username=jose%40doe.com&password=password'}


responce = requests.post("http://127.0.0.1:8000/posts",data=json.dumps(post))

print(responce.json())