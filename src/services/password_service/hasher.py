from argon2 import PasswordHasher, exceptions

ph = PasswordHasher()

def hash_password(password) -> str:
    return ph.hash(password)


def verify_password(hashed_password, password) -> bool:
    try:
        return ph.verify(hashed_password, password)
    except exceptions.VerifyMismatchError:
        return False


# TODO: rehash