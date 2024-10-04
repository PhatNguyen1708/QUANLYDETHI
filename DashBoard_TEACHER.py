from tkinter import *
from tkinter import ttk
from tkinter import Tk
import json
from PIL import Image,ImageTk


class dashBoard_teacher:
    def __init__(self, dB, fullname):
        self.dB=dB
        self.fullname=fullname
        self.dB.geometry('925x700+300+200')
        self.dB.title('Dashboard - Trang chủ giáo viên')
        self.dB.config(bg='white')

        title=Label(self.dB,text='Hệ thống quản lí câu hỏi, đề thi trắc nghiệm',bg='white',fg='#57a1f8', font=('Arial', 20, 'bold')).place(x=260,y=2)

        leftFrame=Frame(self.dB,bd=0,relief=RIDGE, bg='#57a1f8')
        leftFrame.place(x=0, y=0, width=210, height=700)

        self.user_label = Label(self.dB, text=f"Teacher: {self.fullname}", bg='white', fg='#57a1f8', font=('Arial', 12, 'bold'))
        self.user_label.place(relx=1, rely=0, anchor=NE,y=670)


#-------------------------------------- KHỞI TẠO CÁC NÚT LỰA CHỌN MÔN HỌC 

        # self.menuLabel=Label(leftFrame,text='Danh sách môn học',fg='white',bg='#57a1f8',font=('Arial', 15, 'bold'))
        # self.menuLabel.place(x=3,y=0)
        # self.toanButton=Button(leftFrame,text='Toán học',font=('Arial', 15, 'bold'),width=15,bg='white',bd=0,activebackground='#57a1f8',command=self.toanhoc,state='disabled')
        # self.toanButton.place(x=10,y=30)
        # self.vatlyButton=Button(leftFrame,text='Vật lý',font=('Arial', 15, 'bold'),width=15,bg='white',bd=0,activebackground='#57a1f8',command=self.vatly)
        # self.vatlyButton.place(x=10,y=80)
        # self.hoahocButton=Button(leftFrame,text='Hóa học',font=('Arial', 15, 'bold'),width=15,bg='white',bd=0,activebackground='#57a1f8',command=self.hoahoc)
        # self.hoahocButton.place(x=10,y=130)
        # self.sinhhocButton=Button(leftFrame,text='Sinh học',font=('Arial', 15, 'bold'),width=15,bg='white',bd=0,activebackground='#57a1f8',command=self.sinhhoc)
        # self.sinhhocButton.place(x=10,y=180)
        # self.vanButton=Button(leftFrame,text='Ngữ văn',font=('Arial', 15, 'bold'),width=15,bg='white',bd=0,activebackground='#57a1f8',command=self.vanhoc,state='disabled')
        # self.vanButton.place(x=10,y=230)
        # self.anhButton=Button(leftFrame,text='Anh văn',font=('Arial', 15, 'bold'),width=15,bg='white',bd=0,activebackground='#57a1f8',command=self.anhhoc)
        # self.anhButton.place(x=10,y=280)
        # self.suButton=Button(leftFrame,text='Lịch sử',font=('Arial', 15, 'bold'),width=15,bg='white',bd=0,activebackground='#57a1f8',command=self.suhoc)
        # self.suButton.place(x=10,y=330)
        # self.diaButton=Button(leftFrame,text='Địa lý',font=('Arial', 15, 'bold'),width=15,bg='white',bd=0,activebackground='#57a1f8',command=self.diahoc)
        # self.diaButton.place(x=10,y=380)
        # self.gdcdButton=Button(leftFrame,text='GDCD',font=('Arial', 15, 'bold'),width=15,bg='white',bd=0,activebackground='#57a1f8',command=self.gdcdhoc)
        # self.gdcdButton.place(x=10,y=430)

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
        # data=self.load_student_accounts(r'data\Accounts.json')
        # self.insert_resultData(data)
        
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
        # data=self.load_student_accounts(r'data\Accounts.json')
        # self.insert_Data(data)
        
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
            id=user.get("id","")
            fullname = user.get("fullname", "")
            quizzes = user.get("quizzes", [])
            for quiz in quizzes:
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
                self.tree.insert("", "end", text=str(idx), values=(id,fullname, subject, soDe, score, time_completed))
                idx +=1

    def load_student_accounts(self,file_path):
        with open(file_path, "r", encoding="utf-8") as file:
            accounts_data = json.load(file)
        student_accounts = [account for account in accounts_data if account.get("type") == "Student"]
        return student_accounts

    def count_students(self,filepath):
        try:
            with open(filepath, 'r', encoding='utf-8') as file:
                data = json.load(file)
                student_count = sum(1 for user in data if user.get('type', '') == 'Student')
                return student_count
        except FileNotFoundError:
            print("File not found!")
            return 0
    
    def view(self):
        for result in self.tree.get_children():
            self.tree.delete(result)
        self.tree.delete(*self.tree.get_children())
        data=self.load_student_accounts(r'data\Accounts.json')
        self.insert_resultData(data)

#-------------------------------- CÁC FUNC LÀM VIỆC VỚI BẢNG TTHS
    def insert_Data(self, data):
        idx=1
        for i, user in enumerate(data):
            id=user.get("id","")
            fullname = user.get("fullname", "")
            gender = user.get("gender", "")
            lop = user.get("class", "")
            dob = user.get("dob", "")
            address = user.get("address", "")
            self.tree2.insert("", "end", text=str(idx), values=(id,fullname, gender, lop, dob, address))
            idx +=1

#-------------------------------------- CÁC FUNCTION KHI LỰA CHỌN MÔN HỌC
    # def hoahoc(self):
    #     self.window=Toplevel(self.dB)
    #     self.window.destroy()
    #     self.hoahocwindow=hoahoc()

    # def sinhhoc(self):
    #     self.window=Toplevel(self.dB)
    #     self.window.destroy()
    #     self.sinhhocwindow=sinhhoc()

    # def vatly(self):
    #     self.window=Toplevel(self.dB)
    #     self.window.destroy()
    #     self.vatlywindow=vatly()    
    
    # def toanhoc(self):
    #     self.window=Toplevel(self.dB)
    #     self.window.destroy()
    #     self.toanwindow=toan()  

    # def vanhoc(self):
    #     self.window=Toplevel(self.dB)
    #     self.window.destroy()
    #     self.vanwindow=van()  

    # def anhhoc(self):
    #     self.window=Toplevel(self.dB)
    #     self.window.destroy()
    #     self.anhwindow=anh()  

    # def suhoc(self):
    #     self.window=Toplevel(self.dB)
    #     self.window.destroy()
    #     self.suwindow=su()  

    # def diahoc(self):
    #     self.window=Toplevel(self.dB)
    #     self.window.destroy()
    #     self.diawindow=dia()  

    # def gdcdhoc(self):
    #     self.window=Toplevel(self.dB)
    #     self.window.destroy()
    #     self.gdcdwindow=gdcd()  

if __name__ == "__main__":
    menu=Tk()
    obj=dashBoard_teacher(menu,'Dinh Thi Ngoc Tram')
    menu.mainloop()