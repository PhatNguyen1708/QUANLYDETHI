from base64 import encode
from email.charset import Charset
import json
from os import name
import string
import cx_Oracle
from cryptogram import AES_Cipher

class Questions():
    def __init__(self):
        self.questions=[]
        self.aes_cipher = AES_Cipher()
        try:
            self.con = cx_Oracle.connect('CauHoiTracNghiem/123@localhost:1521/free')
            self.cursor = self.con.cursor()
        except cx_Oracle.DatabaseError as er:
            print('There is an error in the Oracle database:',er)
        self.cursor = self.con.cursor()

    def getQues(self, subject_code):
        query = "SELECT MACAUHOI, CAUHOI, DAPANA, DAPANB, DAPANC, DAPAND, DAPAN_DUNG FROM CAUHOI WHERE MAMONHOC = :subject_code"
        self.cursor.execute(query, subject_code = subject_code)
        
        self.questions = []
        
        for row in self.cursor.fetchall():
            print(f"Row data: {row}")
            encrypted_answer = row[6]
            print(f"Raw answer to encrypt: {encrypted_answer}")
            en_answer = self.aes_cipher.encrypt(encrypted_answer)
            print(f"Encrypted answer: {en_answer}")
            question_data = {
                "id": row[0],  # MACAUHOI
                "question": row[1],  # CAUHOI
                "option": [row[2], row[3], row[4], row[5]],  # DAPANA, DAPANB, DAPANC, DAPAND
                "encrypted_answer": en_answer
            }

            self.questions.append(question_data)
    
    # def add_fileJson(self,jsonFilePath):
    #     file=open(jsonFilePath,"r",encoding='utf-8')
    #     y=json.load(file)
    #     for i in y:
    #         self.questions.append(i)

    # def save_question(self,jsonFilePath):
    #     with open(jsonFilePath, 'w',encoding='utf-8') as file:
    #         json.dump(self.questions,file, indent=4)

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
                answer = question_data["encrypted_answer"]
                return question_id,question_text,A,B,C,D, answer
            else:
                return "Invalid question index."

    def count_ques(self):
        return len(self.questions)
    
questions = Questions()
questions.getQues("MH00002")
