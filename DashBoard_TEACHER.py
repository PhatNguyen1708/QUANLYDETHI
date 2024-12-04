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

        self.refreshInfoView()
        self.DSMONHOC()

#-------------------------------------- KHỞI TẠO CÁC NÚT LỰA CHỌN MÔN HỌC 
        self.menuLabel=Label(self.leftFrame,text='Danh sách môn học',fg='white',bg='#57a1f8',font=('Arial', 15, 'bold'))
        self.menuLabel.place(x=10,y=230)

#-------------------------------------- TẠO BẢNG HIỂN THỊ KẾT QUẢ HỌC TẬP HỌC SINH
        scrolly1 = Scrollbar(self.dB,orient='vertical')
        scrollx1 = Scrollbar(self.dB, orient="horizontal")

        self.tableLabel=Label(self.dB,text='---Kết quả học tập của học sinh---', bg='white',fg='black', font=('Arial', 15, 'bold')).place(x=385,y=45)
        self.tree= ttk.Treeview(self.dB,columns=("MSHS","fullname","subject","soDe","score","time_completed"),xscrollcommand=scrollx1.set,yscrollcommand=scrolly1.set)
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
        self.tree.place(x=230,y=85,width=635)
        data=self.load_resultData()
        self.insert_resultData(data)
        
        scrollx1.place(x=230,y=310,width=635)
        scrollx1.config(command=self.tree.xview)

        scrolly1.place(x=865,y=85,height=225)
        scrolly1.config(command=self.tree.yview)

#--------------------- TẠO CHỨC NĂNG TÌM KIẾM BẰNG SỬ DỤNG KEY COMBOBOX
        self.searchButton=Button(self.dB, text='Tìm kiếm',bg='white',command=self.search,activebackground='#57a1f8',font=('Arial',8,'bold'),width=8).place(x=800,y=335)
        self.searchEntry=Entry(self.dB,width=54, bd=2)
        self.searchEntry.place(x=230,y=337)

        self.filter = StringVar()
        self.combobox = ttk.Combobox(self.dB,textvariable=self.filter)
        self.combobox['value']=('MSHS','Họ và tên','Môn học','Mã đề','Thời gian hoàn thành')
        self.combobox.place(x=670,y=335,width=125)

        self.viewButton=Button(self.dB, text='Hiển thị',bg='white',command=self.view,activebackground='#57a1f8',font=('Arial',8,'bold'),width=8).place(x=800,y=365)

        self.countStudentLabel=Label(self.dB,text='Tổng số lượng học sinh: '+ str(self.count_students(r'data\Accounts.json')),bg='white').place(x=230,y=655)

#-------------------------------------- TẠO BẢNG HIỂN THỊ THÔNG TIN HỌC SINH 
        scrolly2 = Scrollbar(self.dB,orient='vertical')
        scrollx2 = Scrollbar(self.dB, orient="horizontal")

        self.tableLabel=Label(self.dB,text='---Danh sách học sinh---', bg='white',fg='black', font=('Arial', 15, 'bold')).place(x=440,y=375)
        self.tree2= ttk.Treeview(self.dB,columns=("id","fullname","gender","lop","dob","address"),xscrollcommand=scrollx2.set,yscrollcommand=scrolly2.set)
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
        self.tree2.place(x=230,y=410,width=635)
        data=self.load_student_accounts()
        self.insert_Data(data)
        
        scrollx2.place(x=230,y=635,width=635)
        scrollx2.config(command=self.tree2.xview)

        scrolly2.place(x=865,y=410,height=225)
        scrolly2.config(command=self.tree2.yview)

        self.helpButton=Button(self.dB, text='?',bg='#57a1f8',fg='black',command=self.help,activebackground='white',font=('Arial',10,'bold'),width=3).place(x=885,y=5)


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

    # def updateInfo(self):
    #     window = Toplevel(self.studentView)
    #     window.title("Cập nhật thông tin ")
    #     window.geometry('450x300+550+350')
    #     window.config(background='white')

    #     updateLabel = Label(window,text='Cập nhật thông tin học sinh', bg='white',  fg='black', font=('Arial', 15, 'bold')).place(x=90,y=10)

    #     fullnameLabel=Label(window,text='Họ và tên: ', bg='white',  fg='black', font=('Times new roman', 13)).place(x=30,y=45)
    #     fullnameEntry=Entry(window,width=35, bg='white',font=('Arial', 13))
    #     fullnameEntry.place(x=110,y=45)
    #     fullnameEntry.insert(0,self.fullName)

    #     idLabel=Label(window,text='Mã số: ' + self.id, bg='white',  fg='black', font=('Times new roman', 13)).place(x=30,y=75)

    #     genderLabel=Label(window,text='Giới tính: ', bg='white',  fg='black', font=('Times new roman', 13)).place(x=200,y=75)
    #     genderEntry=Entry(window,width=16, bg='white',font=('Arial', 13))
    #     genderEntry.place(x=280,y=75)
    #     genderEntry.insert(0,self.gender)


    #     classLabel=Label(window,text='Lớp: ', bg='white',  fg='black', font=('Times new roman', 13)).place(x=30,y=105)
    #     classEntry=Entry(window,width=35, bg='white',font=('Arial', 13))
    #     classEntry.place(x=110,y=105)
    #     classEntry.insert(0,str(self.lop))

    #     dobLabel=Label(window,text='Ngày sinh: ', bg='white',  fg='black', font=('Times new roman', 13)).place(x=30,y=135)
    #     dobEntry=Entry(window,width=35, bg='white',font=('Arial', 13))
    #     dobEntry.place(x=110,y=135)
    #     dobEntry.insert(0,self.dob)

    #     addressLabel=Label(window,text='Địa chỉ: ', bg='white',  fg='black', font=('Times new roman', 13)).place(x=30,y=165)
    #     addressEntry=Entry(window,width=35, bg='white',font=('Arial', 13))
    #     addressEntry.place(x=110,y=165)
    #     addressEntry.insert(0,self.address)

    #     def checkDOB(dob):
    #         ngay_sinh = dob
    #         ngay_hien_tai = datetime.now()
    #         tuoi = ngay_hien_tai.year - ngay_sinh.year - ((ngay_hien_tai.month, ngay_hien_tai.day) < (ngay_sinh.month, ngay_sinh.day))
    #         if tuoi >= 16:
    #             return True
    #         else:
    #             messagebox.showerror('Error','Tuổi không hợp lệ')
    #             return False
            
    #     def checkClass(Class):
    #         # Class = int(Class)
    #         # if Class < 10 or Class > 12:
    #         #     messagebox.showerror('Error','Lớp không hợp lệ')
    #         #     return False
    #         return True

    #     def updateData():
    #         fullname=fullnameEntry.get()
    #         gender=genderEntry.get()
    #         Class=classEntry.get()
    #         dob=dobEntry.get()
    #         dob = datetime.strptime(dob, "%d-%m-%Y")
    #         address=addressEntry.get()
    #         if checkDOB(dob) == True:
    #             self.cur.execute("UPDATE HOCSINH SET HOTENHS = :fullname, GIOITINH = :gender,NGAYSINH = :dob, LOP = :Class, DIACHI = :address WHERE MSHS = :a",{'fullname':fullname,'gender':gender,'Class':Class,'dob': cx_Oracle.Date(dob.year, dob.month, dob.day),'address':address,'a':self.id})
    #             self.con.commit()
    #             userExist=True
    #         if not userExist:
    #                 messagebox.showwarning("Lỗi","Không tìm thấy mã số")
    #         self.refreshInfoView()
    #         window.destroy()
        
    #     updateButton = Button(window,text='Cập nhật thông tin',activebackground='white',bg='#64a587', font=('Arial', 10, 'bold'),command=updateData).place(x=160,y=200)


#-------------------------------- CÁC FUNC LÀM VIỆC VỚI BẢNG KQHT
    def search(self):
        idx=1
        data = self.load_student_accounts(r'data\Accounts.json')
        filterVar = self.filter.get()
        query = self.searchEntry.get().lower()
        self.tree.delete(*self.tree.get_children())
        for i,student in enumerate(data):
            id=student.get('id','')
            fullname=student.get('fullname','')
            for quiz in student.get('quizzes', []):
                score = quiz.get("score", "")
                subject = quiz.get("subject", "")
                if subject == 'hoahoc':
                    subject = 'Hóa học'
                elif subject == 'sinhhoc':
                    subject = 'Sinh học'
                elif subject == 'vatly':
                    subject = 'Vật lý'
                elif subject == 'toan':
                    subject = 'Toán'
                elif subject == 'van':
                    subject = 'Ngữ Văn'
                elif subject == 'anh':
                    subject = 'Tiếng Anh'
                elif subject == 'su':
                    subject = 'Lịch sử'
                elif subject == 'dia':
                    subject = 'Địa lý'
                elif subject == 'gdcd':
                    subject = 'GDCD'
                soDe = quiz.get("soDe", "")
                time_completed = quiz.get("time_completed", "")
                if filterVar == 'Môn học' and query in quiz.get('subject', '').lower():
                    self.tree.insert('', 'end',text=str(idx), values=(id,fullname, subject, soDe, score, time_completed))
                elif filterVar == 'MSHS' and query == student.get('id', '').lower():
                    self.tree.insert('', 'end',text=str(idx), values=(id,fullname, subject, soDe, score, time_completed))
                elif filterVar == 'Họ và tên' and query in student.get('fullname', '').lower():
                    self.tree.insert('', 'end',text=str(idx), values=(id,fullname, subject, soDe, score, time_completed))
                elif filterVar == 'Mã đề' and query == str(quiz.get('soDe','')).lower():
                    self.tree.insert('', 'end',text=str(idx), values=(id,fullname, subject, soDe, score, time_completed))
                elif filterVar == 'Thời gian hoàn thành' and query in quiz.get('time_completed', '').lower():
                    self.tree.insert('', 'end',text=str(idx), values=(id,fullname, subject, soDe, score, time_completed))
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
        data=self.load_student_accounts()
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

    def DSMONHOC(self):
        self.cur.execute('select TENMONHOC from MONHOC,GIAOVIEN where MSGV =:a and GIAOVIEN.MAMONHOC = MONHOC.MAMONHOC',{'a':self.id})
        data = self.cur.fetchall()
        print(data)
        if data == []:
            return
        self.cur.execute('select MAMONHOC from GIAOVIEN where MSGV =:a',{'a':self.id})
        tenmon = self.cur.fetchall()
        button = Button(self.leftFrame,text=data[0][0],font=('Arial', 15, 'bold'),width=15,bg='white',bd=0,activebackground='#57a1f8',command=partial(self.question,tenmon[0][0]))
        button.place(x=10,y=290)
        

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


if __name__ == "__main__":
    menu=Tk()
    obj=dashBoard_teacher(menu,'Trần Thị Kiều','GV0001')
    menu.mainloop()