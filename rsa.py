import random
import pandas as pd
from prime import *

class RSA():
    def __init__(self, message: str):
        self.message = message
        self.private_key = None
        self.public_key = None

    def key_generation(self, num_bits):
        p = generate_prime(num_bits)
        q = generate_prime(num_bits)
        n = p * q # Modulus for both keys
        phi = (p-1) * (q-1)
        
        # Public Key
        e = random.randint(2, phi - 1)
        # e must be coprime with phi -> gcd(e, phi) = 1
        while (not primality_test(e)):
            e = random.randint(2, phi - 1)
        self.public_key = (n, e)

        # Private Key
        d = multiplicative_inverse(e, phi)
        self.private_key = (n, d)

    def encrypt(self):
        # Convert message to numbers
        message_list = [ord(x) for x in self.message]

        # C = M^e mod n
        ciphertext = []
        for x in message_list:
            value = modular_exponentiation(x, self.public_key[1], self.public_key[0])
            ciphertext.append(value)
        self.ciphertext = ciphertext

    def decrypt(self):
        # M = C^d mod n
        decrypted = []
        for x in self.ciphertext:
            value = modular_exponentiation(x, self.private_key[1], self.private_key[0])
            decrypted.append(value)
        
        # Convert decrypted list into string representation
        plaintext = [chr(x) for x in decrypted]
        plaintext = "".join(plaintext)
        self.plaintext =  plaintext

if __name__ == "__main__":
    obj = RSA("Hello world")
    obj.key_generation(512)
    obj.encrypt()
    obj.decrypt()

    print(f"Original message: {obj.message}" + "\n")
    print(f"Public Key: {obj.public_key}" + "\n")
    print(f"Private Key: {obj.private_key}" + "\n")
    print(f"Ciphertext: {obj.ciphertext}" + "\n")
    print(f"Decrypted ciphertext: {obj.plaintext}" + "\n")

