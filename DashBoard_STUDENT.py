from tkinter import *
from tkinter import ttk
from datetime import datetime, timedelta
import json, tkinter, string
from tkinter import messagebox, simpledialog
import cx_Oracle

class dashBoard_student:
    def __init__(self, studentView,fullName,id):
        self.studentView = studentView
        self.fullName=fullName
        self.id=id
        self.gender = ""
        self.lop = ""
        self.dob = ""
        self.address = ""
        self.funtion = None
        self.exam_schedule()

        self.studentView.geometry('925x530+300+200')
        self.studentView.title('Dashboard - Trang chủ học sinh')
        self.studentView.config(bg='white')
        self.studentView.resizable(width=FALSE, height=FALSE)
        try:
            self.con = cx_Oracle.connect('CauHoiTracNghiem/123@localhost:1521/free')
        except cx_Oracle.DatabaseError as er:
            print('There is an error in the Oracle database:',er)
        self.cur = self.con.cursor()

        self.studentInfoView()
        self.refreshInfoView()

        title = Label(self.studentView, text='Hệ thống làm bài tập trắc nghiệm', bg='white', fg='black', font=('Arial', 20, 'bold')).place(x=320, y=0)
#===============================Các chức năng cơ bản
        self.frame_funtion = Frame(self.studentView, bd=0, relief=RIDGE, bg='Silver')
        self.frame_funtion.place(x=0, y=0, width=210, height=530)
        
        self.title_funtion = Label(self.frame_funtion,text="Danh sách chức năng",bg="silver",font=('Arial', 13, 'bold'))
        self.title_funtion.place(x=17,y=10)

        self.updateButton = Button(self.frame_funtion,text='Cập nhật thông tin',activeforeground='white',fg='black',bg='white', font=('Arial', 10, 'bold'),command=self.updateInfo)
        self.updateButton.place(x=10,y=50,width=190,height=30)

        self.exam_resultsButton = Button(self.frame_funtion,text='Kết quả học tập',activeforeground='white',fg='black',bg='white', font=('Arial', 10, 'bold'),command=self.exam_results)
        self.exam_resultsButton.place(x=10,y=90,width=190,height=30)
        
        self.exam_scheduleButton = Button(self.frame_funtion,text='Lịch Thi',activeforeground='white',fg='black',bg='white', font=('Arial', 10, 'bold'),command=self.exam_schedule)
        self.exam_scheduleButton.place(x=10,y=130,width=190,height=30)

        self.helpButton=Button(self.studentView, text='?',bg='#64a587',fg='black',command=self.help,activebackground='white',font=('Arial',10,'bold'),width=3).place(x=885,y=5)


#--------------------------------- KHỞI TẠO BẢNG KẾT QUẢ HỌC TẬP CỦA HỌC SINH
    def exam_results(self):
        #-------kiểm tra xem có cái frame chưa nè
        if self.funtion:
            self.funtion.destroy()

        #-------tạo frame đồ đó
        self.funtion = Frame(self.studentView, bd=0, relief=RIDGE, bg='white',width=712,height=328,highlightbackground="black", highlightthickness=2)
        self.funtion.place(x=210,y=200)

        #-------này là cái scrolling bar nè
        scrolly = Scrollbar(self.funtion,orient='vertical')
        scrollx = Scrollbar(self.funtion, orient="horizontal")

        #-------này là cái bản kết quả
        self.tableLabel=Label(self.funtion,text='----Kết quả học tập----', bg='white',fg='black', font=('Arial', 15, 'bold')).place(x=230,y=0)
        self.tree= ttk.Treeview(self.funtion,columns=("subject","soDe","score","time_completed"),xscrollcommand=scrollx.set,yscrollcommand=scrolly.set)
        self.tree.heading("#0",text='ID')
        self.tree.column("#0",width=45,anchor='nw')
        self.tree.heading("subject",text='Môn học')
        self.tree.column("subject",width=90,anchor='nw')
        self.tree.heading("soDe",text='Mã đề')
        self.tree.column("soDe",width=55,anchor='nw')
        self.tree.heading("score",text='Điểm')
        self.tree.column("score",width=45,anchor='nw')
        self.tree.heading("time_completed",text='Thời gian hoàn thành')
        self.tree.place(x=40,y=30,width=635,height=250)
        
        scrollx.place(x=40,y=280,width=635)
        scrollx.config(command=self.tree.xview)

        scrolly.place(x=675,y=30,height=250)
        scrolly.config(command=self.tree.yview)
        

        self.refreshButton=Button(self.funtion, text='Refresh',bg='#64a587',fg='black',command=self.refresh,activebackground='white',font=('Arial',7,'bold'),width=10).place(x=635,y=300)
      
    def select_subject(self, subject):
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
#--------------------------------- KHỞI TẠO GIAO DIỆN CẬP NHẬT THÔNG TIN HỌC SINH
    def refreshInfoView(self):
        self.cur.execute('select * from HOCSINH')
        data = self.cur.fetchall()
        for student in data:
            if student[0] == self.id:
                self.fullName = student[1]
                if student[2] != None:
                    self.dob = student[2].strftime('%d-%m-%Y')
                else:
                    self.dob = student[2]
                self.gender = student[3]
                self.address = student[4]
                self.lop = student[5]

                self.nameLabel.config(text=f"Họ và tên: {self.fullName}")
                self.classLabel.config(text=f'Lớp: {self.lop}')
                self.genderLabel.config(text=f'Giới tính: {self.gender}')
                self.addressLabel.config(text=f'Địa chỉ thường trú: {self.address}')
                self.dobLabel.config(text=f'Ngày sinh: {self.dob}')
                break

    def updateInfo(self):
        if self.funtion:
            self.funtion.destroy()
        self.funtion = Frame(self.studentView, bd=0, relief=RIDGE, bg='white',width=712,height=328,highlightbackground="black", highlightthickness=2)
        self.funtion.place(x=210,y=200)

        updateLabel = Label(self.funtion,text='Cập nhật thông tin học sinh', bg='white',  fg='black', font=('Arial', 15, 'bold')).place(x=230,y=10)

        fullnameLabel=Label(self.funtion,text='Họ và tên: ', bg='white',  fg='black', font=('Times new roman', 13)).place(x=170,y=45)
        fullnameEntry=Entry(self.funtion,width=35, bg='white',font=('Arial', 13))
        fullnameEntry.place(x=250,y=45)
        fullnameEntry.insert(0,self.fullName)

        idLabel=Label(self.funtion,text='Mã số: ' + self.id, bg='white',  fg='black', font=('Times new roman', 13)).place(x=170,y=75)

        genderLabel=Label(self.funtion,text='Giới tính: ', bg='white',  fg='black', font=('Times new roman', 13)).place(x=340,y=75)
        genderEntry=Entry(self.funtion,width=16, bg='white',font=('Arial', 13))
        genderEntry.place(x=420,y=75)
        if self.gender != None:
            genderEntry.insert(0,self.gender)


        classLabel=Label(self.funtion,text='Lớp: ', bg='white',  fg='black', font=('Times new roman', 13)).place(x=170,y=105)
        classEntry=Entry(self.funtion,width=35, bg='white',font=('Arial', 13))
        classEntry.place(x=250,y=105)
        if self.lop != None:
            classEntry.insert(0,str(self.lop))

        dobLabel=Label(self.funtion,text='Ngày sinh: ', bg='white',  fg='black', font=('Times new roman', 13)).place(x=170,y=135)
        dobEntry=Entry(self.funtion,width=35, bg='white',font=('Arial', 13))
        dobEntry.place(x=250,y=135)
        if self.dob != None:
            dobEntry.insert(0,self.dob)

        addressLabel=Label(self.funtion,text='Địa chỉ: ', bg='white',  fg='black', font=('Times new roman', 13)).place(x=170,y=165)
        addressEntry=Entry(self.funtion,width=35, bg='white',font=('Arial', 13))
        addressEntry.place(x=250,y=165)
        if self.address != None:
            addressEntry.insert(0,self.address)

        def checkDOB(dob):
            ngay_sinh = dob
            ngay_hien_tai = datetime.now()
            tuoi = ngay_hien_tai.year - ngay_sinh.year - ((ngay_hien_tai.month, ngay_hien_tai.day) < (ngay_sinh.month, ngay_sinh.day))
            if tuoi >= 16:
                return True
            else:
                messagebox.showerror('Error','Tuổi không hợp lệ')
                return False
            
        def checkClass(Class):
            # self.cur.execute('select * from HOCSINH')
            # if Class < 10 or Class > 12:
            #     messagebox.showerror('Error','Lớp không hợp lệ')
            #     return False
            return True

        def updateData():
            fullname=fullnameEntry.get()
            gender=genderEntry.get()
            Class=classEntry.get()
            address=addressEntry.get()
            dob=dobEntry.get()
            if dob == "":
                messagebox.showwarning("Lỗi","Vui lòng nhập ngày sinh")
                return
            dob = datetime.strptime(dob, "%d-%m-%Y")
            if checkDOB(dob) == True:
                self.cur.execute("UPDATE HOCSINH SET HOTENHS = :fullname, GIOITINH = :gender,NGAYSINH = :dob, LOP = :Class, DIACHI = :address WHERE MSHS = :a",{'fullname':fullname,'gender':gender,'Class':Class,'dob': cx_Oracle.Date(dob.year, dob.month, dob.day),'address':address,'a':self.id})
                self.con.commit()
                userExist=True
            if not userExist:
                    messagebox.showwarning("Lỗi","Không tìm thấy mã số")
            self.refreshInfoView()
        
        updateButton = Button(self.funtion,text='Cập nhật thông tin',activebackground='white',bg='#64a587', font=('Arial', 10, 'bold'),command=updateData).place(x=300,y=200)

#---------------------------------- TẠO LỊCH THI
    def exam_schedule(self):
         #-------kiểm tra xem có cái frame chưa nè
        if self.funtion:
            self.funtion.destroy()

        #-------tạo frame đồ đó
        self.funtion = Frame(self.studentView, bd=0, relief=RIDGE, bg='white',width=712,height=328,highlightbackground="black", highlightthickness=2)
        self.funtion.place(x=210,y=200)

        



        



#--------------------------------- CÁC FUNCTION LÀM VIỆC VỚI BẢNG KẾT QUẢ
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
    obj = dashBoard_student(studentView,'Nguyễn Thị Thùy Trang','HS00006')
    studentView.mainloop()
