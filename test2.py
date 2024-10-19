import cx_Oracle
from Crypto.Cipher import DES
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import base64
import os

def getData(query):
    try:
        connection = cx_Oracle.connect('CauHoiTracNghiem/123@localhost:1521/free')
        cursor = connection.cursor()

        cursor.execute(query)
        data = cursor.fetchall()
        print("Dữ liệu đã lấy: ", data)
        return data
    except Exception as e:
        print("Lỗi khi kết nối: ", e)

def encrypt_hybrid(data, public_key):
    des_key = os.urandom(8)
    des_cipher = DES.new(des_key, DES.MODE_EAX)
    ciphertext, tag = des_cipher.encrypt_and_digest(data.encode('utf-8'))

    rsa_cipher = PKCS1_OAEP.new(public_key)
    encrypted_key = rsa_cipher.encrypt(des_key)
    
    return {
        'encrypted_key': base64.b64encode(encrypted_key).decode('utf-8'),
        'ciphertext': base64.b64encode(ciphertext).decode('utf-8'),
        'nonce': base64.b64encode(des_cipher.nonce).decode('utf-8'),
        'tag': base64.b64encode(tag).decode('utf-8')
    }

def decrypt_data(encrypted_data, private_key):
    rsa_cipher = PKCS1_OAEP.new(private_key)
    des_key = rsa_cipher.decrypt(base64.b64decode(encrypted_data['encrypted_key']))

    nonce = base64.b64decode(encrypted_data['nonce'])
    des_cipher = DES.new(des_key, DES.MODE_EAX, nonce=nonce)
    
    ciphertext = base64.b64decode(encrypted_data['ciphertext'])
    tag = base64.b64decode(encrypted_data['tag'])

    try:
        plain_text = des_cipher.decrypt_and_verify(ciphertext, tag)
        return plain_text.decode('utf-8')
    except ValueError:
        raise ValueError("Dữ liệu đã bị thay đổi hoặc không hợp lệ.")

def main():
    query = "SELECT HOTENGV FROM GIAOVIEN WHERE MSGV = 'GV0002'"
    data = getData(query)

    if data:
        plain_text = data[0][0]
        
        rsa_key = RSA.generate(2048)
        public_key = rsa_key.publickey()
        
        encrypted_data = encrypt_hybrid(plain_text, public_key)
        
        print("Dữ liệu đã mã hóa:")
        print(encrypted_data)

        decrypted_data = decrypt_data(encrypted_data, rsa_key)
        print("Dữ liệu đã giải mã:", decrypted_data)
    else:
        print("Không tìm thấy dữ liệu.")

if __name__ == "__main__":
    main()
