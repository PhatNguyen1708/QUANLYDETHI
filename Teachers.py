from Questions import *
from tkinter import messagebox
from cryptogram import *

class Teacher(Questions):
    def __init__(self,subject_code):
        super().__init__()
        self.aes_cipher = AES_Cipher()
        self.subject_code = subject_code
        try:
            self.con = cx_Oracle.connect('CauHoiTracNghiem/123@localhost:1521/free')
        except cx_Oracle.DatabaseError as er:
            print('There is an error in the Oracle database:',er)
        self.cur = self.con.cursor()
        
    def add_question_file(self):
        if self.subject_code:
            super().getQues(self.subject_code)
        else:
            print("Mã môn học không tồn tại!")

    def Create(self,id,question, options, answer):
        DAPANA = options[0]
        DAPANB = options[1]
        DAPANC = options[2]
        DAPAND = options[3]
        answer= self.cur.callfunc("f_encryptData", cx_Oracle.STRING, [answer])
        self.cur.execute('insert into CAUHOI (MAMONHOC,MACAUHOI,CAUHOI,DAPANA,DAPANB,DAPANC,DAPAND,DAPAN_DUNG)' 'values (:MAMONHOC,:MACAUHOI,:CAUHOI, :DAPANA,:DAPANB,:DAPANC,:DAPAND,:DAPAN_DUNG)',{'MAMONHOC':self.subject_code,'MACAUHOI':id,'CAUHOI':question,'DAPANA':DAPANA,'DAPANB':DAPANB,'DAPANC':DAPANC,'DAPAND':DAPAND,'DAPAN_DUNG':answer})
        self.con.commit()


    def edit(self,filepath,index,replace):
        if 0 <= index-1 < len(self.questions):
            self.questions[index-1]=replace
        super().save_question(filepath)

    def remove(self,index):
        if 0 <= index-1 < len(self.questions):
            self.questions.remove(self.questions[index-1])
        super().save_question(filepath)




