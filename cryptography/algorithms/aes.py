from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes


def encrypt_file(input_file):
    key = get_random_bytes(32) 
    initialization_vector = get_random_bytes(16)
    cipher = AES.new(key, AES.MODE_CBC, initialization_vector)

    file_data = input_file.read()

    pad_len = 16 - (len(file_data) % 16)
    padded_data = file_data + bytes([pad_len] * pad_len)

    encrypted_data = initialization_vector + cipher.encrypt(padded_data)

    return encrypted_data, key


def decrypt_file(encrypted_file, key):
    initialization_vector = encrypted_file[:16]
    encrypted_data = encrypted_file[16:]

    cipher = AES.new(key, AES.MODE_CBC, initialization_vector)

    decrypted_data = cipher.decrypt(encrypted_data)

    pad_len = decrypted_data[-1]
    decrypted_data = decrypted_data[:-pad_len]
    return decrypted_data
