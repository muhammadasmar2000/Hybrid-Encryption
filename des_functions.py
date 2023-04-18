from tables import *

def to_binary_array(message: str) -> np.ndarray:
    # Pad message with trailing spaces
    while (len(message) % 8) != 0:
        message += " "
    res = []
    for x in message:
        res.append(np.binary_repr(ord(x)).zfill(8))
    res = "".join(res)
    res = list(res)
    res = [int(x) for x in res]
    return np.array(res).astype(int)

def key_to_binary(key: str) -> np.ndarray:
    res = np.binary_repr(int(key)).zfill(64)
    res = [int(x) for x in res]
    return np.array(res).astype(int)

# Returns list of 16 numpy arrays for 16 encryption subkeys
def generate_encryption_keys(key: np.ndarray):
    subkeys = np.zeros((16,48)).astype(int)
    subkey = np.zeros(56).astype(int)
    # Permute with pc_1
    for i in range(len(pc_1)):
        subkey[i] = key[pc_1[i]]
    C = subkey[:28]
    D = subkey[28:]
    for i in range(16):
        if i in [0, 1, 8, 15]:
            # Rotate left one bit
            C = np.roll(C, -1)
            D = np.roll(D, -1)
        else:
            # Rotate left two bits
            C = np.roll(C, -2)
            D = np.roll(D, -2)
        full_array = np.concatenate((C, D), axis=None)
        # Permute with pc_2
        subkey = np.zeros(48).astype(int)
        for j in range(len(pc_2)):
            subkey[j] = full_array[pc_2[j] - 1]
        subkeys[i, :] = subkey[:]
    return subkeys

# Returns list of 16 numpy arrays for 16 decryption subkeys
def generate_decryption_keys(key: np.ndarray):
    subkeys = np.zeros((16,48)).astype(int)
    subkey = np.zeros(56).astype(int)
    # Permute with pc_1
    for i in range(len(pc_1)):
        subkey[i] = key[pc_1[i]]
    C = subkey[:28]
    D = subkey[28:]
    full_array = np.concatenate((C, D), axis = None)
    subkey = np.zeros(48).astype(int)
    for i in range(len(pc_2)):
        subkey[i] = full_array[pc_2[i] - 1]
    subkeys[0, :] = subkey[:]
    for i in range(1, 16):
        if i in [1, 8, 15]:
            # One bit right rotation
            C = np.roll(C, 1)
            D = np.roll(D, 1)
        else:
            # Two bit right rotation
            C = np.roll(C, 2)
            D = np.roll(D, 2)
        # Permute with pc_2
        full_array = np.concatenate((C, D), axis = None)
        subkey = np.zeros(48).astype(int)
        for j in range(len(pc_2)):
            subkey[j] = full_array[pc_2[j] - 1]
        subkeys[i, :] = subkey[:]
    return subkeys

# Use initial or final permutation array to permute text block
def permute(block: np.ndarray, table: np.ndarray) -> np.ndarray:
    res = np.zeros(len(block)).astype(int)
    for i in range(len(block)):
        res[i] = block[table[i] - 1]
    return res

# Feistel Function
def f(right: np.ndarray, subkey: np.ndarray) -> np.ndarray:
    # Expansion
    res = np.zeros(48).astype(int)
    for i in range(len(exp_d)):
        res[i] = right[exp_d[i] - 1]

    # Use the expansion result and xor with subkey
    res = np.bitwise_xor(res, subkey)

    # S-box substitution
    substitution = np.zeros(32).astype(int)
    for i in range(8):
        nums = res[(i*6):((i+1)*6)]
        row = (nums[0] * 2) + nums[5]
        col = (nums[1] * 8) + (nums[2] * 4) + (nums[3] * 2) + (nums[4])
        num = sbox[i, row, col]
        substitution[(i*4):(i+1)*4] = np.array(list(np.binary_repr(num).zfill(4))).astype(int)

    # Permutation with perm table
    res = np.zeros(32).astype(int)
    for i in range(len(perm)):
        res[i] = substitution[perm[i] - 1]
    return res

def binary_to_text(binary: np.ndarray) -> str:
    text = ""
    for i in range(binary.shape[0]):
        for j in range(8):
            char_binary = binary[i, (j*8):(j+1)*8]
            char_binary = "".join([str(x) for x in char_binary])
            text += chr(int(char_binary, 2))
    return text
