from tkinter import *
from tkinter import ttk
from datetime import datetime
import json, tkinter, string
from tkinter import messagebox, simpledialog

class dashBoard_student:
    def __init__(self, studentView,fullName,id):
        self.studentView = studentView
        self.fullName=fullName
        self.id=id
        self.gender = ""
        self.lop = ""
        self.dob = ""
        self.address = ""
        self.studentView.geometry('925x530+300+200')
        self.studentView.title('Dashboard - Trang chủ học sinh')
        self.studentView.config(bg='white')
        self.studentInfoView()
        self.refreshInfoView()

        title = Label(self.studentView, text='Hệ thống làm bài tập trắc nghiệm', bg='white', fg='black', font=('Arial', 20, 'bold')).place(x=320, y=0)

        leftFrame = Frame(self.studentView, bd=0, relief=RIDGE, bg='#64a587')
        leftFrame.place(x=0, y=0, width=210, height=530)

        self.helpButton=Button(self.studentView, text='?',bg='#64a587',fg='black',command=self.help,activebackground='white',font=('Arial',10,'bold'),width=3).place(x=885,y=5)

#--------------------------------- KHỞI TẠO BẢNG KẾT QUẢ HỌC TẬP CỦA HỌC SINH
        scrolly = Scrollbar(self.studentView,orient='vertical')
        scrollx = Scrollbar(self.studentView, orient="horizontal")

        self.tableLabel=Label(self.studentView,text='----Kết quả học tập----', bg='white',fg='black', font=('Arial', 15, 'bold')).place(x=440,y=250)
        self.tree= ttk.Treeview(self.studentView,columns=("subject","soDe","score","time_completed"),xscrollcommand=scrollx.set,yscrollcommand=scrolly.set)
        self.tree.heading("#0",text='ID')
        self.tree.column("#0",width=45,anchor='nw')
        self.tree.heading("subject",text='Môn học')
        self.tree.column("subject",width=90,anchor='nw')
        self.tree.heading("soDe",text='Mã đề')
        self.tree.column("soDe",width=55,anchor='nw')
        self.tree.heading("score",text='Điểm')
        self.tree.column("score",width=45,anchor='nw')
        self.tree.heading("time_completed",text='Thời gian hoàn thành')
        self.tree.place(x=230,y=280,width=635)
        # data=self.load_student_result(r'data\Accounts.json')     
        # self.insert(data)
        
        scrollx.place(x=230,y=505,width=635)
        scrollx.config(command=self.tree.xview)

        scrolly.place(x=865,y=280,height=225)
        scrolly.config(command=self.tree.yview)
        

        self.refreshButton=Button(self.studentView, text='Refresh',bg='#64a587',fg='black',command=self.refresh,activebackground='white',font=('Arial',7,'bold'),width=10).place(x=855,y=505)

#--------------------------- Khởi tạo frame chứa lựa chọn môn học & các func xử lí
        self.menuLabel = Label(leftFrame, text='Danh sách môn học', fg='black', bg='#64a587', font=('Arial', 15, 'bold'))
        self.menuLabel.place(x=3, y=0)
        self.toanButton=Button(leftFrame,text='Toán học',font=('Arial', 15, 'bold'),width=15,bg='white',bd=0,activebackground='#57a1f8',command=lambda: self.select_subject('toan'),state='disabled')
        self.toanButton.place(x=10,y=30)
        self.vatlyButton=Button(leftFrame,text='Vật lý',font=('Arial', 15, 'bold'),width=15,bg='white',bd=0,activebackground='#57a1f8',command=lambda: self.select_subject('vatly'))
        self.vatlyButton.place(x=10,y=80)
        self.hoahocButton=Button(leftFrame,text='Hóa học',font=('Arial', 15, 'bold'),width=15,bg='white',bd=0,activebackground='#57a1f8',command=lambda: self.select_subject('hoahoc'))
        self.hoahocButton.place(x=10,y=130)
        self.sinhhocButton=Button(leftFrame,text='Sinh học',font=('Arial', 15, 'bold'),width=15,bg='white',bd=0,activebackground='#57a1f8',command=lambda: self.select_subject('sinhhoc'))
        self.sinhhocButton.place(x=10,y=180)
        self.vanButton=Button(leftFrame,text='Ngữ văn',font=('Arial', 15, 'bold'),width=15,bg='white',bd=0,activebackground='#57a1f8',command=lambda: self.select_subject('van'),state='disabled')
        self.vanButton.place(x=10,y=230)
        self.anhButton=Button(leftFrame,text='Anh văn',font=('Arial', 15, 'bold'),width=15,bg='white',bd=0,activebackground='#57a1f8',command=lambda: self.select_subject('anh'))
        self.anhButton.place(x=10,y=280)
        self.suButton=Button(leftFrame,text='Lịch sử',font=('Arial', 15, 'bold'),width=15,bg='white',bd=0,activebackground='#57a1f8',command=lambda: self.select_subject('su'))
        self.suButton.place(x=10,y=330)
        self.diaButton=Button(leftFrame,text='Địa lý',font=('Arial', 15, 'bold'),width=15,bg='white',bd=0,activebackground='#57a1f8',command=lambda: self.select_subject('dia'))
        self.diaButton.place(x=10,y=380)
        self.gdcdButton=Button(leftFrame,text='GDCD',font=('Arial', 15, 'bold'),width=15,bg='white',bd=0,activebackground='#57a1f8',command=lambda: self.select_subject('gdcd'))
        self.gdcdButton.place(x=10,y=430)
        

    def select_subject(self, subject): # Yêu cầu nhập số đề
        filepath = f"data/{subject}.json"
        while True:
            self.soDe = simpledialog.askinteger("Chọn số đề", "Nhập số đề bạn muốn làm:", initialvalue=0) 
            if  self.soDe < 0 : 
                messagebox.showerror("Lỗi","Vui lòng nhập số đề lớn hơn 0")
                return
            elif self.soDe > len(filepath): 
                messagebox.showerror("Lỗi","Không tìm thấy mã đề") 
                return
            else:
                break
        if self.soDe is not None:
                self.sub = Toplevel(self.studentView)
                # self.obj=QuizApp(self.sub, filepath, self.soDe, subject,self.id)

#--------------------------------- KHỞI TẠO KHU VỰC HIỂN THỊ THÔNG TIN HỌC SINH
    def studentInfoView(self):
        self.studentInfo = Label(self.studentView,text='Thông tin học sinh', bg='white',  fg='black', font=('Arial', 15, 'bold')).place(x=450,y=50)

        self.nameLabel = Label(self.studentView, text=f"Họ và tên: {self.fullName}", bg='white',  fg='black', font=('Times new roman', 13))
        self.nameLabel.place(x=320,y=80)
        self.idLabel = Label(self.studentView,text=f'MSHS: {self.id}', bg='white',  fg='black', font=('Times new roman', 13))
        self.idLabel.place(x=600,y=80)
        self.classLabel= Label(self.studentView,text=f'Lớp: {self.lop}', bg='white',  fg='black', font=('Times new roman', 13))
        self.classLabel.place(x=320,y=105)
        self.genderLabel = Label(self.studentView,text=f'Giới tính: {self.gender}', bg='white',  fg='black', font=('Times new roman', 13))
        self.genderLabel.place(x=600,y=105)
        self.addressLabel = Label(self.studentView,text=f'Địa chỉ thường trú: {self.address}', bg='white',  fg='black', font=('Times new roman', 13),wraplength=450)
        self.addressLabel.place(x=320,y=155)
        self.dobLabel = Label(self.studentView,text=f'Ngày sinh: {self.dob}', bg='white',  fg='black', font=('Times new roman', 13))
        self.dobLabel.place(x=320,y=130)        
        self.updateButton = Button(self.studentView,text='Cập nhật thông tin',activebackground='white',fg='black',bg='#64a587', font=('Arial', 10, 'bold'),command=self.updateInfo).place(x=480,y=205)
        
#--------------------------------- KHỞI TẠO GIAO DIỆN CẬP NHẬT THÔNG TIN HỌC SINH
    def refreshInfoView(self):
        filepath = r"data\Accounts.json"
        try:
            with open(filepath, 'r', encoding='utf-8') as file:
                data = json.load(file)
        except FileNotFoundError:
            data = []
        for student in data:
            if student.get("id") == self.id:
                self.fullName = student.get("fullname", "")
                self.gender = student.get("gender", "")
                self.lop = student.get("class", "")
                self.dob = student.get("dob", "")
                self.address = student.get("address", "")

                # Cập nhật lại các label
                self.nameLabel.config(text=f"Họ và tên: {self.fullName}")
                self.classLabel.config(text=f'Lớp: {self.lop}')
                self.genderLabel.config(text=f'Giới tính: {self.gender}')
                self.addressLabel.config(text=f'Địa chỉ thường trú: {self.address}')
                self.dobLabel.config(text=f'Ngày sinh: {self.dob}')
                break

    def updateInfo(self):
        window = Toplevel(self.studentView)
        window.title("Cập nhật thông tin học sinh")
        window.geometry('450x300+550+350')
        window.config(background='white')

        updateLabel = Label(window,text='Cập nhật thông tin học sinh', bg='white',  fg='black', font=('Arial', 15, 'bold')).place(x=90,y=10)

        fullnameLabel=Label(window,text='Họ và tên: ', bg='white',  fg='black', font=('Times new roman', 13)).place(x=30,y=45)
        fullnameEntry=Entry(window,width=35, bg='white',font=('Arial', 13))
        fullnameEntry.place(x=110,y=45)
        fullnameEntry.insert(0,self.fullName)

        idLabel=Label(window,text='Mã số: ' + self.id, bg='white',  fg='black', font=('Times new roman', 13)).place(x=30,y=75)

        genderLabel=Label(window,text='Giới tính: ', bg='white',  fg='black', font=('Times new roman', 13)).place(x=200,y=75)
        genderEntry=Entry(window,width=16, bg='white',font=('Arial', 13))
        genderEntry.place(x=280,y=75)
        genderEntry.insert(0,self.gender)


        classLabel=Label(window,text='Lớp: ', bg='white',  fg='black', font=('Times new roman', 13)).place(x=30,y=105)
        classEntry=Entry(window,width=35, bg='white',font=('Arial', 13))
        classEntry.place(x=110,y=105)
        classEntry.insert(0,str(self.lop))

        dobLabel=Label(window,text='Ngày sinh: ', bg='white',  fg='black', font=('Times new roman', 13)).place(x=30,y=135)
        dobEntry=Entry(window,width=35, bg='white',font=('Arial', 13))
        dobEntry.place(x=110,y=135)
        dobEntry.insert(0,self.dob)

        addressLabel=Label(window,text='Địa chỉ: ', bg='white',  fg='black', font=('Times new roman', 13)).place(x=30,y=165)
        addressEntry=Entry(window,width=35, bg='white',font=('Arial', 13))
        addressEntry.place(x=110,y=165)
        addressEntry.insert(0,self.address)

        def checkDOB(dob):
            ngay_sinh = datetime.strptime(dob, "%d/%m/%Y")
            ngay_hien_tai = datetime.now()
            tuoi = ngay_hien_tai.year - ngay_sinh.year - ((ngay_hien_tai.month, ngay_hien_tai.day) < (ngay_sinh.month, ngay_sinh.day))
            if tuoi >= 16:
                return True
            else:
                messagebox.showerror('Error','Tuổi không hợp lệ')
                return False
            
        def checkClass(Class):
            Class = int(Class)
            if Class < 10 or Class > 12:
                messagebox.showerror('Error','Lớp không hợp lệ')
                return False
            return True

        def updateData():
            fullname=fullnameEntry.get()
            gender=genderEntry.get()
            Class=classEntry.get()
            dob=dobEntry.get()
            address=addressEntry.get()
            newData={
                "fullname": fullname,
                "gender": gender,
                "class": Class,
                "dob": dob,
                "address": address
            }
            filepath=r"data\Accounts.json"
            try:
                with open(filepath,'r',encoding='utf-8') as file:
                    data = json.load(file)
            except FileNotFoundError:
                data = []
            userExist = False
            for student in data:
                if student["id"] == self.id and checkDOB(dob) == True and checkClass(Class) == True:
                    student.update(newData)
                    userExist=True
            if not userExist:
                    messagebox.showwarning("Lỗi","Không tìm thấy mã số")
            with open(filepath,'w',encoding='utf-8') as file:
                json.dump(data,file,ensure_ascii=False)

            self.refreshInfoView()
            window.destroy()
        
        updateButton = Button(window,text='Cập nhật thông tin',activebackground='white',bg='#64a587', font=('Arial', 10, 'bold'),command=updateData).place(x=160,y=200)

#--------------------------------- CÁC FUNCTION LÀM VIỆC VỚI BẢNG KẾT QUẢ
    def load_student_result(self, filepath):
        with open(filepath, "r", encoding="utf-8") as file:
            accounts_data = json.load(file)
        student_accounts = [account for account in accounts_data if account.get("type") == "Student" and account.get("id") == self.id]
        return student_accounts
    
    def insert(self,data):
        idx=1
        for i, user in enumerate(data):
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
                self.tree.insert("", "end", text=str(idx), values=(subject, soDe, score, time_completed))
                idx +=1

    def refresh(self):
        for result in self.tree.get_children():
            self.tree.delete(result)
        data=self.load_student_result(r'data\Accounts.json')    
        self.insert(data)

    def help(self):
        window = Toplevel(self.studentView)
        window.title("Hướng dẫn sử đụng")
        window.geometry('450x550+550+350')
        window.config(background='white')

        helpLabel = Label(window,text='Hướng dẫn sử đụng', bg='white',  fg='black', font=('Arial', 15, 'bold')).place(x=90,y=10)
        with open(r'data\student.txt','r',encoding='utf-8') as file:
            content = file.read()

        text = Label(window,text=content,bg='white',justify='left',wraplength=420).place(x=20,y=50)
        

if __name__ == "__main__":
    studentView = Tk()
    obj = dashBoard_student(studentView,'Dinh Thi Ngoc Tram','2033225436')
    studentView.mainloop()