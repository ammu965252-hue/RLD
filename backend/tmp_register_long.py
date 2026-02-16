import requests
url='http://localhost:8000/register'
headers={'Origin':'http://localhost:8003','Content-Type':'application/json'}
data={'full_name':'Long Pass','email':'longpass@example.com','password':'x'*150}
r=requests.post(url,json=data,headers=headers)
print(r.status_code)
print(r.text)
