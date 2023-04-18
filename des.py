from des_functions import *

class DES:
    def __init__(self, message: str, master_key: int):
        self.user_message = message
        self.master_key = master_key

        self.message = to_binary_array(self.user_message) # np.array(0, 1, 0, 1, 1, 0 ...)
        self.master_key = key_to_binary(str(self.master_key)) # np.array(0, 1, 0, 1, 1, 0 ...) with length of 56
        self.message = np.reshape(self.message, (-1, 64))

        # Generate subkeys for encryption and decryption
        self.encrypt_keys = generate_encryption_keys(self.master_key[:])
        self.decrypt_keys = generate_decryption_keys(self.master_key[:])

    def encrypt(self):
        # Encrypt plain text one block at a time
        self.ciphertext = np.zeros(self.message.shape).astype(int)
        for i in range(self.message.shape[0]):
            block = self.message[i, :]
            init_perm = permute(block[:], initial_perm)
            L = init_perm[:32]
            R = init_perm[32:]
            # 16 Rounds of encryption
            for j in range(16):
                new_left = R[:]
                new_right = np.bitwise_xor(L[:], f(R[:], self.encrypt_keys[j, :]))
                L[:] = new_left[:]
                R[:] = new_right[:]
            # Swap left and right halves
            temp = L[:]
            L = R[:]
            R = temp[:]
            full_array = np.concatenate((L, R)).astype(int)
            # Apply final permutation and create ciphertext
            self.ciphertext[i, :] = permute(full_array[:], final_perm)

        # Print binary ciphertext string representation and binary array
        self.ciphertext_text = binary_to_text(self.ciphertext[:, :])

    def decrypt(self):
        # Decrypt cipher text one block at a time
        self.plaintext = np.zeros(self.ciphertext.shape).astype(int)
        for i in range(self.ciphertext.shape[0]):
            block = self.ciphertext[i, :]
            init_perm = permute(block[:], initial_perm)
            L = init_perm[:32]
            R = init_perm[32:]
            # 16 Rounds of decryption
            for j in range(16):
                new_left = R[:]
                new_right = np.bitwise_xor(L[:], f(R[:], self.decrypt_keys[j, :]))
                L[:] = new_left[:]
                R[:] = new_right[:]
            # Swap left and right halves
            temp = L[:]
            L = R[:]
            R = temp[:]
            full_array = np.concatenate((L, R)).astype(int)
            # Apply final permutation
            self.plaintext[i, :] = permute(full_array, final_perm)
        # Print decrypted text in binary and string representation
        self.plaintext_text = binary_to_text(self.plaintext[:, :]).rstrip()

"""
if plaintext_text == user_message:
    print("Decryption Successful")
else:
    print("Decryption Unsuccessful")
"""