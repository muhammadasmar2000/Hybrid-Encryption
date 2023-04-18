import random
from prime import *

class RSA():
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
        # Generate random number for des private key encryption
        des_private_key = random.getrandbits(64)

        # C = M^e mod n
        self.ciphertext = modular_exponentiation(des_private_key, self.public_key[1], self.public_key[0])

    def decrypt(self):
        # M = C^d mod n
        self.plaintext = modular_exponentiation(self.ciphertext, self.private_key[1], self.private_key[0])

