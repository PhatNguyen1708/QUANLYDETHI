import base64
import hashlib
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad 
import binascii

password = "12345678901234567890123456789012"  
iv_hex = "1234567890123456"  

class AES_Cipher:
    BLOCK_SIZE = 16

    def __init__(self):
        self.private_key = password.encode("utf-8")
        self.iv = iv_hex.encode("utf-8")

    def encrypt(self, raw):
        raw = raw.encode("utf-8")
        padded_data = pad(raw, self.BLOCK_SIZE)
        cipher = AES.new(self.private_key, AES.MODE_CBC, self.iv)
        encrypted_data = cipher.encrypt(padded_data)
        return binascii.hexlify(encrypted_data).decode("utf-8").upper()

    def decrypt(self, enc_hex):
        encrypted_data = binascii.unhexlify(enc_hex)
        cipher = AES.new(self.private_key, AES.MODE_CBC, self.iv)
        decrypted_data = cipher.decrypt(encrypted_data)
        return unpad(decrypted_data, self.BLOCK_SIZE).decode("utf-8")  # Loại bỏ padding sau khi giải mã

