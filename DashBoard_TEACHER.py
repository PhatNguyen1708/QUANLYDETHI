from tkinter import *
from tkinter import ttk
from tkinter import Tk
from tkcalendar import DateEntry
import json
from PIL import Image,ImageTk
from tkinter import messagebox, simpledialog
import cx_Oracle
from datetime import datetime
from questionListView import *
from functools import partial
from datetime import datetime, timedelta


class dashBoard_teacher:
    def __init__(self, dB, fullname,id,passWord):
        self.dB=dB
        self.fullname=fullname
        self.id = id
        self.passWord = passWord
        self.gender = ""
        self.dob = ""
        self.frame_data =None

        self.dB.geometry('925x700+300+200')
        self.dB.title('Dashboard - Trang chủ giáo viên')
        self.dB.config(bg='white')
        self.dB.resizable(width=FALSE, height=FALSE)

        try:
            self.con = cx_Oracle.connect(f'{self.id}/{self.passWord}@localhost:1521/free')
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

        b_test = Button(self.leftFrame,text="Tạo đề thi",font=('Arial', 13, 'bold'),width=18,bg='white',bd=0,activebackground='#57a1f8',command=self.make_test)
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
        self.cur.execute('select * from cauhoitracnghiem.GIAOVIEN')
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
                            from cauhoitracnghiem.KETQUA,cauhoitracnghiem.HOCSINH,cauhoitracnghiem.monhoc
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
                            from cauhoitracnghiem.KETQUA,cauhoitracnghiem.HOCSINH,cauhoitracnghiem.monhoc
                            where KETQUA.MSHS=HOCSINH.MSHS and ketqua.mamonhoc = monhoc.mamonhoc''' )
        student_accounts = self.cur.fetchall()
        return student_accounts

    def load_student_accounts(self):
        self.cur.execute('select * from cauhoitracnghiem.HOCSINH')
        student_accounts = self.cur.fetchall()
        return student_accounts

    def count_students(self,filepath):
        self.cur.execute('select * from cauhoitracnghiem.HOCSINH')
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
        obj=Application(teacherView, subject_code,self.id,self.passWord)
        teacherView.mainloop()

    def MONHOC_cua_giao_vien(self):
        self.cur.execute('select TENMONHOC from cauhoitracnghiem.MONHOC,cauhoitracnghiem.GIAOVIEN where MSGV =:a and GIAOVIEN.MAMONHOC = MONHOC.MAMONHOC',{'a':self.id})
        data = self.cur.fetchall()
        if data == []:
            return
        self.cur.execute('select MAMONHOC from cauhoitracnghiem.GIAOVIEN where MSGV =:a',{'a':self.id})
        tenmon = self.cur.fetchall()
        button_mon = Button(self.leftFrame,text=data[0][0],font=('Arial', 15, 'bold'),width=15,bg='white',bd=0,activebackground='#57a1f8',command=partial(self.question,tenmon[0][0]))
        button_mon.place(x=10,y=200)
        return 
        
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
        self.cur.execute("SELECT MAMONHOC FROM cauhoitracnghiem.GIAOVIEN WHERE MSGV = :id", {'id': self.id})
        subject_code = self.cur.fetchone()

        if subject_code:
            subject_code = subject_code[0]

            # Truy vấn câu hỏi theo mã môn học
            self.cur.execute("SELECT MACAUHOI, CAUHOI, DAPANA, DAPANB, DAPANC, DAPAND FROM cauhoitracnghiem.CAUHOI WHERE MAMONHOC = :subject_code", 
                             {'subject_code': subject_code})
            questions = self.cur.fetchall()

            # Hiển thị câu hỏi vào bảng
            for question in questions:
                self.questions_tree.insert('', 'end', values=question)
        else:
            messagebox.showwarning("Thông báo", "Không tìm thấy môn học của giáo viên.")

#-------------------------------------- Bảng tạo đề thi
    def make_test(self):
         #-------kiểm tra xem có cái frame chưa nè
        if self.frame_data:
            self.frame_data.destroy()
            
        self.frame_data = Frame(self.dB,bd=0,relief=RIDGE, bg='white')
        self.frame_data.place(x=210, y=40, width=715, height=661)
        l_exam_schedule_frame = Label(self.frame_data,text='---Danh sách học sinh---', bg='white',fg='black', font=('Arial', 15, 'bold')).place(x=230,y=10)

        self.exam_schedule_frame()
        self.add_exam_frame()
    
    def add_exam_frame(self):

        self.cur.execute('select MAMONHOC from cauhoitracnghiem.GIAOVIEN where MSGV =:a',{'a':self.id})
        mamon = self.cur.fetchall()[0][0]

        self.exam_schedule = Frame(self.frame_data, bd=0, relief=RIDGE, bg='white',width=680,height=300,highlightbackground="black")
        self.exam_schedule.place(x=20,y=350)

        l_tab_add = Label(self.exam_schedule,text='---Tạo Đề thi---', bg='white',fg='black', font=('Arial', 15, 'bold')).place(x=270,y=10)

        listheader = ['Mã đề','Số câu hỏi']

        self.made = Label(self.exam_schedule,text="Danh sách mã đề")
        self.made.place(x=300,y=50)

        self.list_made =ttk.Treeview(self.exam_schedule, selectmode="extended", columns=listheader, show="headings")

        scrolly = ttk.Scrollbar(self.exam_schedule, orient="vertical", command=self.list_made.yview)

        self.list_made.configure(yscrollcommand=scrolly.set)

        self.list_made.place(x=300,y=70,width=180,height=100)
        scrolly.place(x=480,y=70,height=100)

        self.list_made.heading(0, text='Mã', anchor=NW)
        self.list_made.heading(1, text='Số câu hỏi', anchor=NW)
        
        self.list_made.column(0, width=70,minwidth=70,anchor='nw')    
        self.list_made.column(1, width=50,minwidth=50,anchor='nw')

        l_made = Label(self.exam_schedule,text="Mã đề:")
        l_made.place(x=30,y=70)

        e_made = Entry(self.exam_schedule,width=10, bg='white',font=('Arial', 13))
        e_made.place(x=80,y=70)

        l_date = Label(self.exam_schedule,text="Ngày làm bài:")
        l_date.place(x=30,y=100)

        e_date = DateEntry(self.exam_schedule, width=15, background='black',foreground='white', borderwidth=2, date_pattern='dd-mm-y')
        e_date.place(x=120,y=100)

        l_time = Label(self.exam_schedule,text="Giờ bài:")
        l_time.place(x=30,y=130)

        hour_start = Spinbox(self.exam_schedule,from_=0,to=23,width=5)
        hour_start.place(x=100,y=130)

        m_start = Spinbox(self.exam_schedule,from_=0,to=59,width=5)
        m_start.place(x=150,y=130)

        var = StringVar(value="Thêm")

        c_update = Radiobutton(self.exam_schedule,text="Cập nhật",variable=var,value="Cập nhật",bg="white")
        c_update.place(x=30,y=180)

        c_add = Radiobutton(self.exam_schedule,text="Thêm",variable=var,value="Thêm",bg="white")
        c_add.place(x=150,y=180)

        def check_tontai(made,time):
            self.cur.execute('select MADETHI,THOIGIAN_BATDAU from cauhoitracnghiem.DETHI_MONHOC where MAMONHOC=:MAMONHOC',{'MAMONHOC':mamon})
            for cur in self.cur:
                    if made == cur[0]:
                        return False
            self.cur.execute('select MADETHI,THOIGIAN_BATDAU from cauhoitracnghiem.DETHI_MONHOC')
            for cur in self.cur:
                if made == cur[0] and datetime.strptime(time, "%d-%m-%Y %H:%M") == cur[1]:
                    return False
            return True


        def add_dethi():
            made = e_made.get()
            date = e_date.get()
            hour = hour_start.get()
            minute = m_start.get()
            time = date + " "+ hour+":"+minute
            if made == "":
                messagebox.showerror("Lỗi","Vui Lòng nhập mã đề")
                return
            elif made not in self.load_made():
                messagebox.showerror("Lỗi","Vui Lòng nhập mã đề hợp lệ")
                return
            if var.get() == "Thêm":
                if not check_tontai(made,time):
                    messagebox.showerror("Lỗi","Mã đề đã tồn tại")
                    return
                else:
                    self.cur.execute("""ALTER SESSION SET NLS_TIMESTAMP_FORMAT = 'DD-MM-YYYY HH24:MI:SS'""")
                    self.cur.execute("""insert into cauhoitracnghiem.DETHI_MONHOC (MADETHI,MAMONHOC,THOIGIAN_BATDAU)
                                        values (:MADETHI, :MAMONHOC,:THOIGIAN_BATDAU)""",{'MADETHI':made,'MAMONHOC':mamon,'THOIGIAN_BATDAU':time})
            else:
                self.cur.execute("""ALTER SESSION SET NLS_TIMESTAMP_FORMAT = 'DD-MM-YYYY HH24:MI:SS'""")
                self.cur.execute("""UPDATE cauhoitracnghiem.DETHI_MONHOC SET THOIGIAN_BATDAU= :time
                                 where MADETHI = :MADETHI and MAMONHOC = :MAMONHOC""",
                                 {'MADETHI':made,'MAMONHOC':mamon,'time':time})
            self.con.commit()
            self.get_schedule()
                

        b_add_update = Button(self.exam_schedule,text="Thêm hoặc chỉnh sửa",command=add_dethi)
        b_add_update.place(x=150,y=210)

        self.load_made()
    
    def load_made(self):
        self.cur.execute('''select *
                            from cauhoitracnghiem.DeThi''')
        rows = self.cur.fetchall()
        rows = list(rows)
        made = []
        for row in rows:
            self.list_made.insert("", "end",values=(row[0],row[1]))
            made.append(row[0])
        return made

    def exam_schedule_frame(self):
        self.exam_schedule = Frame(self.frame_data, bd=0, relief=RIDGE, bg='white',width=712,height=310,highlightbackground="black")
        self.exam_schedule.place(x=20,y=40)
        self.exam_schedule.grid_propagate(False)

        canvas= Canvas(self.exam_schedule,width=650,height=290,background="white")
        scrolly=ttk.Scrollbar(self.exam_schedule, orient='vertical', command=canvas.yview)
        scrollx=ttk.Scrollbar(self.exam_schedule, orient='horizontal', command=canvas.xview)
        self.scrollyFrame=Frame(canvas,background="white")
        scrolly.pack(side='right', fill='y')
        scrollx.pack(side='bottom', fill='x')
        canvas.pack(side='left', fill='both', expand=True)
        canvas.create_window((0,0), window=self.scrollyFrame, anchor='nw')
        canvas.configure(yscrollcommand=scrolly.set)
        self.scrollyFrame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        self.schedule_labels = []
        self.day_in_weak = []
        self.var = IntVar(self.exam_schedule)

        self.current_date = datetime.now()

        self.days = ["Thứ 2", "Thứ 3", "Thứ 4", "Thứ 5", "Thứ 6", "Thứ 7", "Chủ nhật"]
        self.schedule_data = {i: {"morning": [], "afternoon": [], "evening": []} for i in range(2, 9)}  # Monday=2, Sunday=8

        def create_time_slots():
            periods = ["Sáng (1-6)", "Chiều (7-12)", "Tối (13-15)"]
            for i, period in enumerate(periods):
                label = Label(self.scrollyFrame, text=period, font=("Arial", 9), padx=10, pady=10, relief="ridge", bg="lightyellow", height=3)
                label.grid(row=i + 2, column=0, sticky="nsew")

        def update_calendar():
            for label in self.schedule_labels:
                label.destroy()
            self.schedule_labels = []
            self.day_in_weak = []
            start_of_week = self.current_date - timedelta(days=self.current_date.weekday())
            for i in range(7):
                date = start_of_week + timedelta(days=i)
                label = Label(self.scrollyFrame, text=self.days[i] + '\n' + date.strftime("%d/%m/%Y"), font=("Arial", 10), relief="ridge",width=9)
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

        self.header_frame = Frame(self.scrollyFrame)
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
                            from cauhoitracnghiem.DETHI_MONHOC , cauhoitracnghiem.MONHOC
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
        for widget in self.exam_schedule.grid_slaves():
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
                        self.scrollyFrame,
                        text=f"{subject_info['subject']}\n{subject_info['id_subject']}\nTiết: {subject_info['periodStart']}",
                        font=("Arial", 10),
                        padx=5,
                        pady=5,
                        relief="ridge",
                        bg="lightpink" if self.var.get() == 1 else "lightblue"
                    )
                    schedule_label.grid(row=row, column=col, sticky="nsew", pady=5, ipadx=5, ipady=8)
                    self.schedule_labels.append(schedule_label)

if __name__ == "__main__":
    menu=Tk()
    obj=dashBoard_teacher(menu,'Trần Thị Kiều','GV0001',123)
    menu.mainloop()