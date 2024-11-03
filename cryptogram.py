import base64
import hashlib
from Crypto.Cipher import AES
from Crypto import Random


password = "yewhsaklQO28318NV"

class AES_Cipher:
    BLOCK_SIZE = 16

    def __init__(self):
        self.private_key = hashlib.sha256(password.encode("utf-8")).digest()
    
    def pad(self, s):
        padding = self.BLOCK_SIZE - len(s) % self.BLOCK_SIZE
        return s + (padding * chr(padding))
    
    def unpad(self, s):
        return s[:-ord(s[len(s) - 1:])]

    def encrypt(self, raw):
        raw = self.pad(raw)
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(self.private_key, AES.MODE_CBC, iv)
        encrypted_data = iv + cipher.encrypt(raw.encode("utf-8"))
        return base64.b64encode(encrypted_data).decode("utf-8")

    def decrypt(self, enc):
        enc = base64.b64decode(enc)
        iv = enc[:16]
        cipher = AES.new(self.private_key, AES.MODE_CBC, iv)
        decrypted_data = cipher.decrypt(enc[16:])
        return self.unpad(decrypted_data.decode("utf-8"))