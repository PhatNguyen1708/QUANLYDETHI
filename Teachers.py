from Questions import *
from tkinter import messagebox
from cryptogram import *

class Teacher(Questions):
    def __init__(self,subject_code,id,passwd):
        self.id = id
        self.passwd = passwd
        super().__init__(id,passwd)
        self.aes_cipher = AES_Cipher()
        self.subject_code = subject_code
        try:
            self.con = cx_Oracle.connect(f'{self.id}/{self.passwd}@localhost:1521/free')
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
        answer= self.cur.callfunc("CauHoiTracNghiem.CRYPTO.RSA_ENCRYPT", cx_Oracle.STRING, [answer,'MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCeautJPn9t6V5NcncuX7DHZdG+j/Hlfl9au9wmkjk1Tv85zf8FgmSKmnl/7vX5/+Gp8rbBamWETDX1akykeyKrS4uuYwFa4IPglvzAGGeLwd6N61uIZTb79nDECTf95/9ot2DepqFbzZrk4aoVR8vLPC/jduQcT7EFmkV13ZnrVwIDAQAB'])
        self.cur.execute('insert into CauHoiTracNghiem.CAUHOI (MAMONHOC,MACAUHOI,CAUHOI,DAPANA,DAPANB,DAPANC,DAPAND,DAPAN_DUNG)' 
                         'values (:MAMONHOC,:MACAUHOI,:CAUHOI, :DAPANA,:DAPANB,:DAPANC,:DAPAND,:DAPAN_DUNG)',
                         {'MAMONHOC':self.subject_code,'MACAUHOI':id,'CAUHOI':question,'DAPANA':DAPANA,'DAPANB':DAPANB,'DAPANC':DAPANC,'DAPAND':DAPAND,'DAPAN_DUNG':answer})
        self.con.commit()


    def edit(self,id,question, options, answer):
        DAPANA = options[0]
        DAPANB = options[1]
        DAPANC = options[2]
        DAPAND = options[3]
        answer= self.cur.callfunc("CauHoiTracNghiem.CRYPTO.RSA_ENCRYPT", cx_Oracle.STRING, [answer,'MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCeautJPn9t6V5NcncuX7DHZdG+j/Hlfl9au9wmkjk1Tv85zf8FgmSKmnl/7vX5/+Gp8rbBamWETDX1akykeyKrS4uuYwFa4IPglvzAGGeLwd6N61uIZTb79nDECTf95/9ot2DepqFbzZrk4aoVR8vLPC/jduQcT7EFmkV13ZnrVwIDAQAB'])
        self.cur.execute('UPDATE CauHoiTracNghiem.CAUHOI SET CAUHOI =:CAUHOI, DAPANA =:DAPANA,DAPANB =:DAPANB,DAPANC =:DAPANC,DAPAND =:DAPAND,DAPAN_DUNG =:DAPAN_DUNG WHERE MAMONHOC =:MAMONHOC AND MACAUHOI =:MACAUHOI',
                         {'MAMONHOC':self.subject_code,'MACAUHOI':id,'CAUHOI':question,'DAPANA':DAPANA,'DAPANB':DAPANB,'DAPANC':DAPANC,'DAPAND':DAPAND,'DAPAN_DUNG':answer})
        self.con.commit()

    def remove(self,id):
        self.cur.execute('delete from CauHoiTracNghiem.CAUHOI where MAMONHOC = :MAMONHOC and MACAUHOI = :MACAUHOI',{'MAMONHOC':self.subject_code,'MACAUHOI':id})
        self.con.commit()




