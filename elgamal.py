import random


def generate_key(p=170141183460469231731687303715884105727):
    g = random.randint(2, p - 2)  # Generator
    x = random.randint(2, p - 2)  # Private key
    h = pow(g, x, p)              # Public key
    return (p, g, h), x

def encrypt(string,public_key):
    p, g, h = public_key
    cipher_text = []
    k = random.randint(2, p - 2)
    for char in string:
        m = ord(char)
        c1 = pow(g, k, p)
        c2 = (m * pow(h, k, p)) % p
        cipher_text.append((c1, c2))
    return cipher_text

def decrypt(encrypted_string, public_key, private_key):
    p, _, _ = public_key
    plain_text = ''
    for c1, c2 in encrypted_string:
        s = pow(c1, p - 1 - private_key, p)
        m = (c2 * s) % p
        plain_text += chr(m)
    return plain_text
