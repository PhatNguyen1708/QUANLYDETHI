from base64 import encode
from email.charset import Charset
import json
from os import name
import string
from cryptogram import *
import cx_Oracle

class Questions():
    def __init__(self,id,passwd):
        self.questions=[]
        self.id =id
        self.passwd =passwd 
        self.aes_cipher = AES_Cipher()
        self.rsa_cipher = RSA_Cipher()
        try:
            self.con = cx_Oracle.connect(f'{id}/{passwd}@localhost:1521/free')
            self.cursor = self.con.cursor()
        except cx_Oracle.DatabaseError as er:
            print('There is an error in the Oracle database:',er)
        self.cursor = self.con.cursor()

    def getQues(self, subject_code):
        query = "SELECT MACAUHOI, CAUHOI, DAPANA, DAPANB, DAPANC, DAPAND, DAPAN_DUNG FROM CauHoiTracNghiem.CAUHOI WHERE MAMONHOC = :subject_code"
        self.cursor.execute(query, subject_code = subject_code)
        
        self.questions = []
        
        for row in self.cursor.fetchall():
            answer = self.cur.callfunc("CauHoiTracNghiem.CRYPTO.RSA_DECRYPT", cx_Oracle.STRING, [row[6],'MIICdwIBADANBgkqhkiG9w0BAQEFAASCAmEwggJdAgEAAoGBAJ5q60k+f23pXk1ydy5fsMdl0b6P8eV+X1q73CaSOTVO/znN/wWCZIqaeX/u9fn/4anytsFqZYRMNfVqTKR7IqtLi65jAVrgg+CW/MAYZ4vB3o3rW4hlNvv2cMQJN/3n/2i3YN6moVvNmuThqhVHy8s8L+N25BxPsQWaRXXdmetXAgMBAAECgYBjhQGossV08/1VJAqxLFYu/c0FLQKmzHv00T2dUZD051q5IqsJ9/9Xf3HCqAkI8/H9RMgAu+lockQXl57sWZrOBDLCFsNP32Q3FJC6iSILv+QKq9g5xa0SZgy0i/s9jQeqcgjIaX/eM30/hct02qBWSxjvrrYDdKFkzMa6GXe3MQJBAPvvp5zhsRNSgB1oyc5AZNDfpahtWlTKKvQ4uBp9SaT0rXZVXW026pYIyT7ICzh/cseYPQU4TOAmx34P1g1vXLkCQQCg+RbJxWlnZElh+2KKBTJO6DIc66uWP8kS439HHnsHrxAuU9K9dw3dOIm80Xh4wo/izFlMxPYAc2H32YfcPiCPAkEA2eVbCHrC1j1ihQ0ejX5wM59a/aMmn3MDV5q+0FpQGZVteY03csAugHk05VHLMqA4O5zWGe+pvayMmeFEdvY8MQJBAJm/0Gg/ygEa5IxVkzTI6dg8J0FAR89mdSM5b2P6VQBt0UKuhWa5w+A8FDLoz+xnyQ6Sp+iPZ3fevQACIaXXITkCQBsFfjhKTH875WHKDD7oKFdkfo6kZV3E7OQ0c3jdsZDmBm1doPLPlHKjpd39YeNklGcK2LNDnaLerI7t2iQi52Q='])
            question_data = {
                "id": row[0],  # MACAUHOI
                "question": row[1],  # CAUHOI
                "option": [row[2], row[3], row[4], row[5]],  # DAPANA, DAPANB, DAPANC, DAPAND
                "answer": answer
            }

            self.questions.append(question_data)
    
    def display_question(self, index):
            if 0 <= index < len(self.questions):
                question_data = self.questions[index]
                question_id = question_data["id"]
                question_text = question_data["question"]
                options = (question_data["option"])
                A=options[0]
                B=options[1]
                C=options[2]
                D=options[3]
                answer = question_data["answer"]
                return question_id,question_text,A,B,C,D, answer

    def count_ques(self):
        return len(self.questions)