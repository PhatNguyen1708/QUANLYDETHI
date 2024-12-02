import base64
import hashlib
from Crypto.PublicKey import RSA
from Crypto.Cipher import AES,PKCS1_OAEP
from Crypto.Util.Padding import pad, unpad
import binascii

import os
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.asymmetric import rsa, padding as asymmetric_padding
from cryptography.hazmat.primitives.ciphers import Cipher
from cryptography.hazmat.primitives.ciphers.algorithms import AES
from cryptography.hazmat.primitives.ciphers.modes import CBC
from cryptography.hazmat.primitives.hashes import SHA256

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


default_aes_key = b'\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0a\x0b\x0c\x0d\x0e\x0f\x10' \
                  b'\x11\x12\x13\x14\x15\x16\x17\x18\x19\x1a\x1b\x1c\x1d\x1e\x1f\x20'

print(f"Default AES Key: {default_aes_key.hex()}")
# RSA & AES
class Hybrid_Cipher:
    def hybrid_encrypt(plaintext, public_key):
        pkcs7_padder = padding.PKCS7(AES.block_size).padder()
        padder_plaintext = pkcs7_padder.update(plaintext) + pkcs7_padder.finalize()

        key = default_aes_key
        print(f"AES Key (default): {key.hex()}")
        iv = os.urandom(128 // 8)

        aes_cbc_cipher = Cipher(AES(key), CBC(iv))
        ciphertext = aes_cbc_cipher.encryptor().update(padder_plaintext)

        oaep_padding = asymmetric_padding.OAEP(mgf=asymmetric_padding.MGF1(algorithm=SHA256()), algorithm=SHA256(), label=None)
        cipherkey = public_key.encrypt(key, oaep_padding)
        print(f"Encrypted AES Key: {cipherkey.hex()}")

        return {'iv': iv, 'ciphertext': ciphertext}, cipherkey
    
    def hybrid_decrypt(ciphertext, cipherkey, private_key):
        oaep_padding = asymmetric_padding.OAEP(mgf=asymmetric_padding.MGF1(algorithm=SHA256()), algorithm=SHA256(), label=None)
        recovered_key = private_key.decrypt(cipherkey, oaep_padding)

        aes_cbc_cipher = Cipher(AES(recovered_key), CBC(ciphertext['iv']))
        recovered_padded_plaintext = aes_cbc_cipher.decryptor().update(ciphertext['ciphertext'])

        pkcs7_unpadder = padding.PKCS7(AES.block_size).unpadder()
        recovered_plaintext = pkcs7_unpadder.update(recovered_padded_plaintext) + pkcs7_unpadder.finalize()
        print(f"Decrypted AES Key: {recovered_key.hex()}")

        return recovered_plaintext




if __name__ == "__main__":
    # cipher = RSA_Cipher()

    # message = "1"
    # encrypted_message = cipher.encrypt(message)
    # print(f"Encrypted: {encrypted_message}")

    # decrypted_message = cipher.decrypt(encrypted_message)
    # print(f"Decrypted: {decrypted_message}")


    # aes_cipher = AES_Cipher()
    # encrypted = aes_cipher.encrypt("1")
    # print(f"Encrypted: {encrypted}")
    # decrypted = aes_cipher.decrypt(encrypted)
    # print(f"Decrypted: {decrypted}")

    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048
    )

    public_key = private_key.public_key()
    plaintext = b'hello every'

    ciphertext, cipherkey = Hybrid_Cipher.hybrid_encrypt(plaintext, public_key)

    print(f"Ciphertext: {ciphertext}")
    print(f"Cipherkey: {cipherkey}")

    try:
        recovered_plaintext = Hybrid_Cipher.hybrid_decrypt(ciphertext, cipherkey, private_key)
    except KeyError as e:
        print(f"KeyError: {e}. Check ciphertext structure.")
    except Exception as e:
        print(f"Unexpected error: {e}")

    assert recovered_plaintext == plaintext
    print("Encryption and decryption successful!")
