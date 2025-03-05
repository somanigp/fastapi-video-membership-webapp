from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError


def generate_hash(pwd_raw):
    ph = PasswordHasher()  # Creating hashing class
    return ph.hash(pwd_raw)  # Using hash function of the class to create hash


def verify_hash(pwd_hash, pwd_raw):
    ph = PasswordHasher()  # Creating hashing class
    verified = False 
    msg = ""
    try:
        verified = ph.verify(pwd_hash, pwd_raw)
    except VerifyMismatchError:
        verified = False
        msg = "Invalid Password"
    except Exception as e:
        verified = False
        msg = f"Unexpected Error : \n{e}"
    return verified, msg
    

# ph.verify(hash, "correct horse battery staple")

