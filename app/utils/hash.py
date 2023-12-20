from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def pass_incryptor(pwd: str):
    hashed_pwd = pwd_context.hash(pwd)
    return hashed_pwd


def verify_password(plain_pwd=None, hashed_pwd=None):
    if plain_pwd != None and hashed_pwd != None:
        return pwd_context.verify(plain_pwd, hashed_pwd)
    return False
    