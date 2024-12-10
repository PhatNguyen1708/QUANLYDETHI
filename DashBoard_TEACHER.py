from tkinter import *
from tkinter import ttk
from tkinter import Tk
import json
from PIL import Image,ImageTk
from tkinter import messagebox, simpledialog
import cx_Oracle
from datetime import datetime
from questionListView import *
from functools import partial


class dashBoard_teacher:
    def __init__(self, dB, fullname,id):
        self.dB=dB
        self.fullname=fullname
        self.id = id
        self.gender = ""
        self.dob = ""
        self.frame_data =None

        self.dB.geometry('925x700+300+200')
        self.dB.title('Dashboard - Trang chủ giáo viên')
        self.dB.config(bg='white')
        self.dB.resizable(width=FALSE, height=FALSE)

        try:
            self.con = cx_Oracle.connect('CauHoiTracNghiem/123@localhost:1521/free')
        except cx_Oracle.DatabaseError as er:
            print('There is an error in the Oracle database:',er)
        self.cur = self.con.cursor()

        title=Label(self.dB,text='Hệ thống quản lí câu hỏi, đề thi trắc nghiệm',bg='white',fg='#57a1f8', font=('Arial', 20, 'bold')).place(x=260,y=2)

        self.leftFrame=Frame(self.dB,bd=0,relief=RIDGE, bg='#57a1f8')
        self.leftFrame.place(x=0, y=0, width=210, height=700)

        self.inflable = Label(self.leftFrame, bg='white', fg='#57a1f8',justify = "left", font=('Arial', 12, 'bold'),width=18,height=8)
        self.inflable.place(x=10, y=20)

        self.nameLabel = Label(self.leftFrame, text=f"Họ và tên: \n{self.fullname}",fg='#57a1f8',justify = "left", font=('Arial', 12, 'bold'))
        self.nameLabel.place(x=10, y=20)

        self.idLabel = Label(self.leftFrame, text=f"MSGV: {self.id}", bg='white', fg='#57a1f8',justify = "left", font=('Arial', 12, 'bold'))
        self.idLabel.place(x=10, y=70)

        self.genderLabel = Label(self.leftFrame, text=f"Giới Tính: {self.gender}", bg='white', fg='#57a1f8',justify = "left", font=('Arial', 12, 'bold'))
        self.genderLabel.place(x=10, y=100)

        self.dobLabel = Label(self.leftFrame, text=f"Ngày sinh: {self.dob}", bg='white', fg='#57a1f8',justify = "left", font=('Arial', 12, 'bold'))
        self.dobLabel.place(x=10, y=130)

        b_student = Button(self.leftFrame,text="Danh Sách Học Sinh",font=('Arial', 13, 'bold'),width=18,bg='white',bd=0,activebackground='#57a1f8',command=self.show_student)
        b_student.place(x=10,y=250)

        b_test = Button(self.leftFrame,text="Tạo đề thi",font=('Arial', 13, 'bold'),width=18,bg='white',bd=0,activebackground='#57a1f8',command=self.show_student)
        b_test.place(x=10,y=290)

        self.refreshInfoView()
        self.MONHOC_cua_giao_vien()
        self.show_student()
#-------------------------------------- TẠO BẢNG HIỂN THỊ KẾT QUẢ HỌC TẬP HỌC SINH
    def show_student(self):
        if self.frame_data:
            self.frame_data.destroy()
        self.frame_data = Frame(self.dB,bd=0,relief=RIDGE, bg='white')
        self.frame_data.place(x=210, y=40, width=715, height=661)

        scrolly1 = Scrollbar(self.frame_data,orient='vertical')
        scrollx1 = Scrollbar(self.frame_data, orient="horizontal")

        self.tableLabel=Label(self.frame_data,text='---Kết quả học tập của học sinh---', bg='white',fg='black', font=('Arial', 15, 'bold')).place(x=175,y=5)
        self.tree= ttk.Treeview(self.frame_data,columns=("MSHS","fullname","subject","soDe","score","time_completed"),xscrollcommand=scrollx1.set,yscrollcommand=scrolly1.set)
        self.tree.heading("#0",text='ID')
        self.tree.column("#0",width=45,anchor='nw')
        self.tree.heading("MSHS",text='MSHS')
        self.tree.column("MSHS",width=95,anchor='nw')
        self.tree.heading("fullname",text='Họ và tên')
        self.tree.heading("subject",text='Môn học')
        self.tree.column("subject",width=90,anchor='nw')
        self.tree.heading("soDe",text='Mã đề')
        self.tree.column("soDe",width=55,anchor='nw')
        self.tree.heading("score",text='Điểm')
        self.tree.column("score",width=45,anchor='nw')
        self.tree.heading("time_completed",text='Thời gian hoàn thành')
        self.tree.place(x=20,y=45,width=635)
        data=self.load_resultData()
        self.insert_resultData(data)
        
        scrollx1.place(x=20,y=270,width=635)
        scrollx1.config(command=self.tree.xview)

        scrolly1.place(x=655,y=45,height=225)
        scrolly1.config(command=self.tree.yview)

#--------------------- TẠO CHỨC NĂNG TÌM KIẾM BẰNG SỬ DỤNG KEY COMBOBOX
        self.searchButton=Button(self.frame_data, text='Tìm kiếm',bg='white',command=self.search,activebackground='#57a1f8',font=('Arial',8,'bold'),width=8).place(x=590,y=295)
        self.searchEntry=Entry(self.frame_data,width=54, bd=2)
        self.searchEntry.place(x=20,y=297)

        self.filter = StringVar()
        self.combobox = ttk.Combobox(self.frame_data,textvariable=self.filter)
        self.combobox['value']=('MSHS','Họ và tên','Môn học','Mã đề','Thời gian hoàn thành')
        self.combobox.current(0)
        self.combobox.place(x=460,y=295,width=125)

        self.viewButton=Button(self.frame_data, text='Hiển thị',bg='white',command=self.view,activebackground='#57a1f8',font=('Arial',8,'bold'),width=8).place(x=590,y=325)

        self.countStudentLabel=Label(self.frame_data,text='Tổng số lượng học sinh: '+ str(self.count_students(r'data\Accounts.json')),bg='white').place(x=20,y=615)

#-------------------------------------- TẠO BẢNG HIỂN THỊ THÔNG TIN HỌC SINH 
        scrolly2 = Scrollbar(self.frame_data,orient='vertical')
        scrollx2 = Scrollbar(self.frame_data, orient="horizontal")

        self.tableLabel=Label(self.frame_data,text='---Danh sách học sinh---', bg='white',fg='black', font=('Arial', 15, 'bold')).place(x=230,y=335)
        self.tree2= ttk.Treeview(self.frame_data,columns=("id","fullname","gender","lop","dob","address"),xscrollcommand=scrollx2.set,yscrollcommand=scrolly2.set)
        self.tree2.heading("#0",text='ID')
        self.tree2.column("#0",width=45,anchor='nw')
        self.tree2.heading("id",text='MSHS')
        self.tree2.column("id",width=95,anchor='nw')
        self.tree2.heading("fullname",text='Họ và tên')
        self.tree2.heading("gender",text='Giới tính')
        self.tree2.column("gender",width=90,anchor='nw')
        self.tree2.heading("lop",text='Lớp')
        self.tree2.column("lop",width=55,anchor='nw')
        self.tree2.heading("dob",text='Ngày sinh')
        self.tree2.heading("address",text='Địa chỉ')
        self.tree2.place(x=20,y=370,width=635)
        data=self.load_student_accounts()
        self.insert_Data(data)
        
        scrollx2.place(x=20,y=595,width=635)
        scrollx2.config(command=self.tree2.xview)

        scrolly2.place(x=655,y=370,height=225)
        scrolly2.config(command=self.tree2.yview)

        self.helpButton=Button(self.frame_data, text='?',bg='#57a1f8',fg='black',command=self.help,activebackground='white',font=('Arial',10,'bold'),width=3).place(x=885,y=5)

    def help(self):
        window = Toplevel(self.dB)
        window.title("Hướng dẫn sử đụng")
        window.geometry('550x700+550+200')
        window.config(background='white')

        helpLabel = Label(window,text='Hướng dẫn sử đụng', bg='white',  fg='black', font=('Arial', 15, 'bold')).place(x=90,y=10)
        with open(r'data\teacher.txt','r',encoding='utf-8') as file:
            content = file.read()

        text = Label(window,text=content,bg='white',justify='left',wraplength=520).place(x=20,y=50)

#-------------------------------- CÁC FUNC CẬP NHẬT THÔNG TIN CỦA GIÁO VIÊN
    def refreshInfoView(self):
        self.cur.execute('select * from GIAOVIEN')
        data = self.cur.fetchall()
        for teacher in data:
            if teacher[0] == self.id:
                self.fullName = teacher[1]
                if teacher[2] != None:
                    self.dob = teacher[2].strftime('%d-%m-%Y')
                else:
                    self.dob = teacher[2]
                self.gender = teacher[3]

                self.nameLabel.config(text=f"Họ và tên: \n{self.fullName}")
                self.genderLabel.config(text=f'Giới tính: {self.gender}')
                self.dobLabel.config(text=f'Ngày sinh: {self.dob}')
                break
#-------------------------------- CÁC FUNC LÀM VIỆC VỚI BẢNG KQHT
    def search(self):
        idx=1
        filterVar = self.filter.get()
        search = self.searchEntry.get()
        query = ('''select KETQUA.MSHS,HOTENHS,TENMONHOC,MADETHI,DIEMTHI,THOIGIAN_HOANTHANH 
                            from KETQUA,HOCSINH,monhoc
                            where KETQUA.MSHS=HOCSINH.MSHS and ketqua.mamonhoc = monhoc.mamonhoc''' )
        if filterVar == 'Môn học':
            query += " AND TENMONHOC = :1"
        elif filterVar == 'MSHS' :
            query += " AND KETQUA.MSHS = :1"
        elif filterVar == 'Họ và tên' :
            query += " AND HOTENHS LIKE '%' || :1 || '%'"
        elif filterVar == 'Mã đề':
            query += " AND MADETHI LIKE '%' || :1 || '%'"
        elif filterVar == 'Thời gian hoàn thành':
            query += " AND THOIGIAN_HOANTHANH LIKE '%' || :1 || '%'"

        if filterVar !="":
            self.cur.execute(query,{'1':search})
        else:
            self.cur.execute(query)

        for result in self.tree.get_children():
            self.tree.delete(result)

        for row in self.cur:
            self.tree.insert("", "end", text=str(idx), values=(row[0],row[1], row[2], row[3], row[4], row[5]))
            idx+=1

    def insert_resultData(self, data):
        idx=1
        for i, user in enumerate(data):
            id=user[0]
            fullname = user[1]
            subject = user[2]
            soDe = user[3]
            score = user[4]
            time_completed = user[5]
            self.tree.insert("", "end", text=str(idx), values=(id,fullname, subject, soDe, score, time_completed))
            idx +=1

    def load_resultData(self):
        self.cur.execute('''select KETQUA.MSHS,HOTENHS,TENMONHOC,MADETHI,DIEMTHI,THOIGIAN_HOANTHANH 
                            from KETQUA,HOCSINH,monhoc
                            where KETQUA.MSHS=HOCSINH.MSHS and ketqua.mamonhoc = monhoc.mamonhoc''' )
        student_accounts = self.cur.fetchall()
        return student_accounts

    def load_student_accounts(self):
        self.cur.execute('select * from HOCSINH')
        student_accounts = self.cur.fetchall()
        return student_accounts

    def count_students(self,filepath):
        self.cur.execute('select * from HOCSINH')
        student_accounts = self.cur.fetchall()
        if len(student_accounts)!=0:
            return len(student_accounts)
        else:
            return 0
    
    def view(self):
        for result in self.tree.get_children():
            self.tree.delete(result)
        self.tree.delete(*self.tree.get_children())
        data=self.load_resultData()
        self.insert_resultData(data)

#-------------------------------- CÁC FUNC LÀM VIỆC VỚI BẢNG TTHS
    def insert_Data(self, data):
        idx=1
        for i, user in enumerate(data):
            id=user[0]
            fullname = user[1]
            gender = user[3]
            lop = user[5]
            dob = user[2].strftime('%d-%m-%Y')
            address = user[4]
            self.tree2.insert("", "end", text=str(idx), values=(id,fullname, gender, lop, dob, address))
            idx +=1

#-------------------------------------- CÁC FUNCTION KHI LỰA CHỌN MÔN HỌC
    def question(self,subject_code):
        self.window=Toplevel(self.dB)
        self.window.destroy()
        teacherView=Tk()
        obj=Application(teacherView, subject_code)
        teacherView.mainloop()

    def MONHOC_cua_giao_vien(self):
        self.cur.execute('select TENMONHOC from MONHOC,GIAOVIEN where MSGV =:a and GIAOVIEN.MAMONHOC = MONHOC.MAMONHOC',{'a':self.id})
        data = self.cur.fetchall()
        print(data)
        if data == []:
            return
        self.cur.execute('select MAMONHOC from GIAOVIEN where MSGV =:a',{'a':self.id})
        tenmon = self.cur.fetchall()
        button_mon = Button(self.leftFrame,text=data[0][0],font=('Arial', 15, 'bold'),width=15,bg='white',bd=0,activebackground='#57a1f8',command=partial(self.question,tenmon[0][0]))
        button_mon.place(x=10,y=200)
        
    def query_questions(self):
        question_window = Toplevel(self.dB)
        question_window.title("Truy vấn câu hỏi")
        question_window.geometry('600x400+400+200')
        question_window.config(bg='white')

        # Nhãn tiêu đề
        titleLabel = Label(question_window, text='Danh sách câu hỏi', bg='white', fg='black', 
                           font=('Arial', 15, 'bold')).pack(pady=10)

        # Bảng để hiển thị câu hỏi
        self.questions_tree = ttk.Treeview(question_window, columns=("MACAUHOI", "CAUHOI", "DAPANA", "DAPANB", "DAPANC", "DAPAND"), show='headings')
        self.questions_tree.heading("MACAUHOI", text='Mã câu hỏi')
        self.questions_tree.heading("CAUHOI", text='Câu hỏi')
        self.questions_tree.heading("DAPANA", text='Đáp án A')
        self.questions_tree.heading("DAPANB", text='Đáp án B')
        self.questions_tree.heading("DAPANC", text='Đáp án C')
        self.questions_tree.heading("DAPAND", text='Đáp án D')

        self.questions_tree.pack(fill=BOTH, expand=True)

        # Thực hiện truy vấn câu hỏi từ cơ sở dữ liệu
        self.load_questions()

    def load_questions(self):
        # Lấy mã môn học của giáo viên từ cơ sở dữ liệu
        self.cur.execute("SELECT MAMONHOC FROM GIAOVIEN WHERE MSGV = :id", {'id': self.id})
        subject_code = self.cur.fetchone()

        if subject_code:
            subject_code = subject_code[0]

            # Truy vấn câu hỏi theo mã môn học
            self.cur.execute("SELECT MACAUHOI, CAUHOI, DAPANA, DAPANB, DAPANC, DAPAND FROM CAUHOI WHERE MAMONHOC = :subject_code", 
                             {'subject_code': subject_code})
            questions = self.cur.fetchall()

            # Hiển thị câu hỏi vào bảng
            for question in questions:
                self.questions_tree.insert('', 'end', values=question)
        else:
            messagebox.showwarning("Thông báo", "Không tìm thấy môn học của giáo viên.")

#-------------------------------------- Bảng tạo đề thi
    def make_test(self):
        if self.frame_data:
            self.frame_data.destroy()
        self.frame_data = Frame(self.dB,bd=0,relief=RIDGE, bg='red')
        self.frame_data.place(x=210, y=40, width=715, height=661)

        

if __name__ == "__main__":
    menu=Tk()
    obj=dashBoard_teacher(menu,'Trần Thị Kiều','GV0001')
    menu.mainloop()