from tkinter import *
from tkinter import ttk
from datetime import datetime, timedelta
import json, tkinter, string
from tkinter import messagebox, simpledialog
import cx_Oracle
from DoTest import QuizApp

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

        self.studentView.geometry('925x530+300+200')
        self.studentView.title('Dashboard - Trang chủ học sinh')
        self.studentView.config(bg='white')
        self.studentView.resizable(width=FALSE, height=FALSE)
        try:
            self.con = cx_Oracle.connect('CauHoiTracNghiem/123@localhost:1521/free')
        except cx_Oracle.DatabaseError as er:
            print('There is an error in the Oracle database:',er)
        self.cur = self.con.cursor()

        self.exam_schedule()
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
        

        self.refreshButton=Button(self.funtion, text='Refresh',bg='#64a587',fg='black',command=self.exam_results,activebackground='white',font=('Arial',7,'bold'),width=10).place(x=635,y=300)
      
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
        self.funtion.place(x=240,y=200)

        self.schedule_labels = []
        self.day_in_weak = []
        self.var = IntVar(self.funtion)

        self.current_date = datetime.now()

        self.days = ["Thứ 2", "Thứ 3", "Thứ 4", "Thứ 5", "Thứ 6", "Thứ 7", "Chủ nhật"]
        self.schedule_data = {i: {"morning": [], "afternoon": [], "evening": []} for i in range(2, 9)}  # Monday=2, Sunday=8

        def create_time_slots():
            periods = ["Sáng (1-6)", "Chiều (7-12)", "Tối (13-15)"]
            for i, period in enumerate(periods):
                label = Label(self.funtion, text=period, font=("Arial", 12), padx=10, pady=10, relief="ridge", bg="lightyellow", height=3)
                label.grid(row=i + 2, column=0, sticky="nsew")

        def update_calendar():
            for label in self.schedule_labels:
                label.destroy()
            self.schedule_labels = []
            self.day_in_weak = []
            start_of_week = self.current_date - timedelta(days=self.current_date.weekday())
            for i in range(7):
                date = start_of_week + timedelta(days=i)
                label = Label(self.funtion, text=self.days[i] + '\n' + date.strftime("%d/%m/%Y"), font=("Arial", 10), relief="ridge",width=9)
                label.grid(row=1, column=i + 1, sticky="nsew")
                self.day_in_weak.append(label)
            
            self.date_label.config(text=f"Tuần {start_of_week.strftime('%d/%m')} - {(start_of_week + timedelta(days=6)).strftime('%d/%m')}")
            self.get_schedule()

        def show_prev_week():
            # Hàm tạo lệnh quay về tuần trước
            self.current_date -= timedelta(weeks=1)
            update_calendar()
    
        def show_next_week():
            # Hàm tạo lệnh quay về tuần sau
            self.current_date += timedelta(weeks=1)
            update_calendar()

        self.header_frame = Frame(self.funtion)
        self.header_frame.grid(row=0, column=0, columnspan=9)

        prev_button = Button(self.header_frame, text="Tuần trước",command=show_prev_week)
        prev_button.grid(row=0, column=0, padx=10)
        
        self.date_label = Label(self.header_frame, text="")
        self.date_label.grid(row=0, column=1, padx=10)
        
        next_button = Button(self.header_frame, text="Tuần sau",command=show_next_week)
        next_button.grid(row=0, column=2, padx=10)
        update_calendar()
        create_time_slots()

    def get_schedule(self):
        self.schedule_data = {i: {"morning": [], "afternoon": [], "evening": []} for i in range(2, 9)}
        self.cur.execute('''select TENMONHOC,THOIGIAN_BATDAU, MONHOC.MAMONHOC
                            from DETHI_MONHOC , MONHOC
                            where MONHOC.MAMONHOC = DETHI_MONHOC.MAMONHOC''')
        rows = self.cur.fetchall()
        rows = list(rows)
        for data in self.day_in_weak:
            chuoi = data.cget("text")
            dong1, dong2=chuoi.strip().split('\n')
            if dong1 != "Chủ nhật":
                thu, so =  dong1.split()
            else:
                so = 8
            for time in rows:
                if time[1] != None:
                    if time[1].strftime("%d/%m/%Y") == dong2:
                        if 6 <= int(time[1].strftime("%H")) <= 12:
                            session = "morning"   
                        elif 12 <= int(time[1].strftime("%H")) <= 17:
                            session = "afternoon"    
                        else:
                            session = "evening"   
                        
                        # Lưu thông tin môn học
                        self.schedule_data[int(so)][session].append({
                            "subject": time[0],
                            "periodStart": int(time[1].strftime("%H")),
                            "id_subject": time[2]
                        })

                        self.display_schedule()
                        

    def display_schedule(self):
        for widget in self.funtion.grid_slaves():
            if int(widget.grid_info()["row"]) >= 2 and int(widget.grid_info()["column"]) >= 1:
                widget.destroy()

        # Hiển thị lịch
        for day, periods in self.schedule_data.items():
            col = day-1 # Từ T2-CN tương ứng với các cột

            for period, subjects in periods.items():
                row = 2 if period == "morning" else 3 if period == "afternoon" else 4
                for subject_info in subjects:
                    # Tạo nhãn cho mỗi môn học
                    schedule_label = Label(
                        self.funtion,
                        text=f"{subject_info['subject']}\n{subject_info['id_subject']}\nTiết: {subject_info['periodStart']}",
                        font=("Arial", 10),
                        padx=5,
                        pady=5,
                        relief="ridge",
                        bg="lightpink" if self.var.get() == 1 else "lightblue"
                    )
                    schedule_label.bind('<Double-1>',lambda event: self.select_subject(schedule_label))
                    schedule_label.grid(row=row, column=col, sticky="nsew", pady=5, ipadx=5, ipady=10)
                    self.schedule_labels.append(schedule_label)


    def select_subject(self,data):
        chuoi = data.cget("text")
        temmon , mamon, tiet = chuoi.strip().split('\n')

        current_time = datetime.now()

        self.cur.execute('select THOIGIAN_BATDAU from DETHI_MONHOC where MAMONHOC=:MAMONHOC',{'MAMONHOC':mamon})
        specific_time = self.cur.fetchall()[0][0]

        if current_time < specific_time:
            messagebox.showwarning(f"Chưa tới giờ",f"Chưa tới giờ làm bài. Thời gian làm bài là {specific_time}")
        elif current_time > specific_time and int((current_time - specific_time).total_seconds() // 60) > 10:
            messagebox.showwarning(f"Trễ Giờ",f"Đã quá giờ làm bài. Thời gian làm bài là {specific_time}")
        elif current_time > specific_time:
            minutes_late = int((current_time - specific_time).total_seconds() // 60)
            id_hs = self.id
            sub = Tk()
            self.obj=QuizApp(sub, 'DT00001', mamon,id_hs,minutes_late)
            self.studentView.destroy()
            sub.mainloop()
        else:
            id_hs = self.id
            sub = Tk()
            self.obj=QuizApp(sub, 'DT00001', mamon,id_hs,0)
            self.studentView.destroy()
            sub.mainloop()




#--------------------------------- CÁC FUNCTION LÀM VIỆC VỚI BẢNG KẾT QUẢ
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
