from passlib.context import CryptContext
import traceback
ctx=CryptContext(schemes=['bcrypt_sha256','bcrypt'], deprecated='auto')
print('schemes:', ctx.schemes())
try:
    print('hashing sample...')
    print(ctx.hash('short_test_pwd'))
except Exception:
    traceback.print_exc()
