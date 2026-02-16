import requests, uuid, sys

base = 'http://localhost:8000'
email = f"test_{uuid.uuid4().hex[:8]}@example.com"
pwd = 'Secur3Pass!23'

print('TEST EMAIL:', email)

try:
    r = requests.post(f'{base}/register', json={'full_name':'Smoke Test','email':email,'password':pwd}, timeout=10)
    print('REGISTER STATUS:', r.status_code)
    print('REGISTER BODY:', r.text)
except Exception as e:
    print('REGISTER EXCEPTION:', repr(e))
    sys.exit(2)

try:
    s = requests.post(f'{base}/login', json={'email':email,'password':pwd}, timeout=10)
    print('LOGIN STATUS:', s.status_code)
    print('LOGIN BODY:', s.text)
except Exception as e:
    print('LOGIN EXCEPTION:', repr(e))
    sys.exit(3)
