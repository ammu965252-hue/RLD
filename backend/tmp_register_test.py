import requests
url='http://localhost:8000/register'
data={'full_name':'Test User','email':'test@example.com','password':'Password123'}
r=requests.post(url,json=data)
print(r.status_code)
print(r.text)
