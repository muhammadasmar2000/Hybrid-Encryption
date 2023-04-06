import random
import pandas as pd

# Miller-Rabin Probabilistic Primality Test
# Return True if n is prime, False otherwise
def primality_test(n: int, t = 40) -> bool:
    r = n - 1
    s = 0
    # Find s and t such that: n - 1 = (2 ^ s) * r
    while (r & 1) == 0:
        r >>= 1
        s += 1
    # Perform primality test 't' times
    for _ in range(t):
        a = random.randint(2, n - 2)
        y = modular_exponentiation(a, r, n)
        if y != 1 and y != (n - 1):
            j = 1
            while j < s and y != n-1:
                y = modular_exponentiation(y, 2, n)
                if y == 1:
                    return False
                j += 1
            if y != n-1:
                return False
    return True

# Uses the square and multiply algorithm for modular exponentiation
def modular_exponentiation(base, power, modulus):
    res = 1
    base = base % modulus    
    if (base == 0) :
        return 0
    while (power > 0) :
        if ((power & 1) == 1):
            res = (res * base) % modulus
        power = power >> 1
        base = (base ** 2) % modulus    
    return int(res)

def multiplicative_inverse(num: int, modulus: int) -> int:
    a = max(num, modulus)
    b = min(num, modulus)
    dict = {
        "A": a,
        "B": b,
        "Q": a // b,
        "R": a % b,
        "T1": 0,
        "T2": 1,
        "T": -1
    }
    while dict["R"] != 0:
        dict["A"] = dict["B"]
        dict["B"] = dict["R"]
        dict["T1"] = dict["T2"]
        dict["T2"] = dict["T"]
        dict["Q"] = dict["A"] // dict["B"]
        dict["R"] = dict["A"] % dict["B"]
        dict["T"] = dict["T1"] - (dict["T2"] * dict["Q"])
    return int(dict["T2"])

def generate_prime(num_bits):
    p = random.getrandbits(num_bits)
    while (not primality_test(p)):
        p = random.getrandbits(num_bits)
    return p