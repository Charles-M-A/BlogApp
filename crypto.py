from cryptography.fernet import Fernet


def encrypt(bytes):
    key = b'Nz0Xcsw_up4R6oJA8OqqI34dnRYvPM_pVAgabBNE4xE='
    f = Fernet(key)
    cipher = f.encrypt(bytes)
    return cipher.decode()


def decrypt(cipher):
    key = b'Nz0Xcsw_up4R6oJA8OqqI34dnRYvPM_pVAgabBNE4xE='
    f = Fernet(key)
    decoded = f.decrypt(cipher)
    return decoded