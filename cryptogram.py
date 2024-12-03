import base64
import hashlib
from Crypto.PublicKey import RSA
from Crypto.Cipher import AES,PKCS1_OAEP
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
        return unpad(decrypted_data, self.BLOCK_SIZE).decode("utf-8")


class RSA_Cipher:
    def __init__(self, key_size = 1024):
        self.key_pair = RSA.generate(key_size)
        self.public_key = b"""-----BEGIN PUBLIC KEY-----
MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCeautJPn9t6V5NcncuX7DHZdG+j/Hlfl9au9wmkjk1Tv85zf8FgmSKmnl/7vX5/+Gp8rbBamWETDX1akykeyKrS4uuYwFa4IPglvzAGGeLwd6N61uIZTb79nDECTf95/9ot2DepqFbzZrk4aoVR8vLPC/jduQcT7EFmkV13ZnrVwIDAQAB
-----END PUBLIC KEY-----"""
        self.private_key = b"""-----BEGIN RSA PRIVATE KEY-----
MIICdwIBADANBgkqhkiG9w0BAQEFAASCAmEwggJdAgEAAoGBAJ5q60k+f23pXk1ydy5fsMdl0b6P8eV+X1q73CaSOTVO/znN/wWCZIqaeX/u9fn/4anytsFqZYRMNfVqTKR7IqtLi65jAVrgg+CW/MAYZ4vB3o3rW4hlNvv2cMQJN/3n/2i3YN6moVvNmuThqhVHy8s8L+N25BxPsQWaRXXdmetXAgMBAAECgYBjhQGossV08/1VJAqxLFYu/c0FLQKmzHv00T2dUZD051q5IqsJ9/9Xf3HCqAkI8/H9RMgAu+lockQXl57sWZrOBDLCFsNP32Q3FJC6iSILv+QKq9g5xa0SZgy0i/s9jQeqcgjIaX/eM30/hct02qBWSxjvrrYDdKFkzMa6GXe3MQJBAPvvp5zhsRNSgB1oyc5AZNDfpahtWlTKKvQ4uBp9SaT0rXZVXW026pYIyT7ICzh/cseYPQU4TOAmx34P1g1vXLkCQQCg+RbJxWlnZElh+2KKBTJO6DIc66uWP8kS439HHnsHrxAuU9K9dw3dOIm80Xh4wo/izFlMxPYAc2H32YfcPiCPAkEA2eVbCHrC1j1ihQ0ejX5wM59a/aMmn3MDV5q+0FpQGZVteY03csAugHk05VHLMqA4O5zWGe+pvayMmeFEdvY8MQJBAJm/0Gg/ygEa5IxVkzTI6dg8J0FAR89mdSM5b2P6VQBt0UKuhWa5w+A8FDLoz+xnyQ6Sp+iPZ3fevQACIaXXITkCQBsFfjhKTH875WHKDD7oKFdkfo6kZV3E7OQ0c3jdsZDmBm1doPLPlHKjpd39YeNklGcK2LNDnaLerI7t2iQi52Q=MIICdwIBADANBgkqhkiG9w0BAQEFAASCAmEwggJdAgEAAoGBAJ5q60k+f23pXk1ydy5fsMdl0b6P8eV+X1q73CaSOTVO/znN/wWCZIqaeX/u9fn/4anytsFqZYRMNfVqTKR7IqtLi65jAVrgg+CW/MAYZ4vB3o3rW4hlNvv2cMQJN/3n/2i3YN6moVvNmuThqhVHy8s8L+N25BxPsQWaRXXdmetXAgMBAAECgYBjhQGossV08/1VJAqxLFYu/c0FLQKmzHv00T2dUZD051q5IqsJ9/9Xf3HCqAkI8/H9RMgAu+lockQXl57sWZrOBDLCFsNP32Q3FJC6iSILv+QKq9g5xa0SZgy0i/s9jQeqcgjIaX/eM30/hct02qBWSxjvrrYDdKFkzMa6GXe3MQJBAPvvp5zhsRNSgB1oyc5AZNDfpahtWlTKKvQ4uBp9SaT0rXZVXW026pYIyT7ICzh/cseYPQU4TOAmx34P1g1vXLkCQQCg+RbJxWlnZElh+2KKBTJO6DIc66uWP8kS439HHnsHrxAuU9K9dw3dOIm80Xh4wo/izFlMxPYAc2H32YfcPiCPAkEA2eVbCHrC1j1ihQ0ejX5wM59a/aMmn3MDV5q+0FpQGZVteY03csAugHk05VHLMqA4O5zWGe+pvayMmeFEdvY8MQJBAJm/0Gg/ygEa5IxVkzTI6dg8J0FAR89mdSM5b2P6VQBt0UKuhWa5w+A8FDLoz+xnyQ6Sp+iPZ3fevQACIaXXITkCQBsFfjhKTH875WHKDD7oKFdkfo6kZV3E7OQ0c3jdsZDmBm1doPLPlHKjpd39YeNklGcK2LNDnaLerI7t2iQi52Q=
-----END RSA PRIVATE KEY-----"""


    def encrypt(self, message):
        if not isinstance(message, str):
            raise ValueError("Message must be a string")
        public_key_obj = RSA.import_key(self.public_key)
        cipher = PKCS1_OAEP.new(public_key_obj)
        encrypted_message = cipher.encrypt(message.encode('utf-8'))
        return base64.b64encode(encrypted_message).decode('utf-8')
    
    def decrypt(self, encrypted_message):
        private_key_obj = RSA.import_key(self.private_key)
        cipher = PKCS1_OAEP.new(private_key_obj)
        decode_encrypted_message = base64.b64decode(encrypted_message.encode('utf-8'))
        # if len(decode_encrypted_message) != 128:  # 128 byte cho khóa RSA 1024 bit
        #     raise ValueError("Ciphertext has an incorrect length")
        decrypted_message = cipher.decrypt(decode_encrypted_message)
        return decrypted_message.decode('utf-8')
    
    def get_public_key(self):
        return self.public_key.decode()
    
    def get_private_key(self):
        return self.private_key.decode()

if __name__ == "__main__":
    # cipher = RSA_Cipher()

    # message = "1"
    # encrypted_message = cipher.encrypt(message)
    # print(f"Encrypted: {encrypted_message}")

    # decrypted_message = cipher.decrypt(encrypted_message)
    # print(f"Decrypted: {decrypted_message}")


    aes_cipher = AES_Cipher()
    encrypted = aes_cipher.encrypt("1")
    print(f"Encrypted: {encrypted}")
    decrypted = aes_cipher.decrypt(encrypted)
    print(f"Decrypted: {decrypted}")
   