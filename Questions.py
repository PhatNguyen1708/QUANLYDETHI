from base64 import encode
from email.charset import Charset
import json
from os import name
import string
import cx_Oracle

class Questions():
    def __init__(self):
        self.questions=[]
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
            de_answer = self.cursor.callfunc("f_decryptData", cx_Oracle.STRING, [row[6]])
            question_data = {
                "id": row[0],  # MACAUHOI
                "question": row[1],  # CAUHOI
                "option": [row[2], row[3], row[4], row[5]],  # DAPANA, DAPANB, DAPANC, DAPAND
                "answer": ord(de_answer[0]) - 65
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
                answer = chr(65 + question_data["answer"])
                return question_id,question_text,A,B,C,D, answer
            else:
                return "Invalid question index."

    def count_ques(self):
        return len(self.questions)