import tkinter as tk
import cx_Oracle
from tkinter import messagebox
from datetime import datetime, timedelta

class ExamScheduler:
    def __init__(self, root):
        self.root = root
        self.root.title("Exam Scheduler")
        self.var = tk.IntVar()
        self.schedule_labels = []
        self.day_in_weak = []
        try:
            self.con = cx_Oracle.connect('CauHoiTracNghiem/123@localhost:1521/free')
            self.cur = self.con.cursor()
        except cx_Oracle.DatabaseError as er:
            print('There is an error in the Oracle database:', er)
        
        # Khởi tạo ngày hiện tại bằng ngày của hệ thống
        self.current_date = datetime.now()
        
        # Tạo frame chức các thông tin, chức năng điều chỉnh ngày tháng
        self.header_frame = tk.Frame(self.root)
        self.header_frame.grid(row=0, column=0, columnspan=9)
        
        prev_button = tk.Button(self.header_frame, text="Tuần trước", command=self.show_prev_week)
        prev_button.grid(row=0, column=0, padx=10)
        
        self.date_label = tk.Label(self.header_frame, text="")
        self.date_label.grid(row=0, column=1, padx=10)
        
        next_button = tk.Button(self.header_frame, text="Tuần sau", command=self.show_next_week)
        next_button.grid(row=0, column=2, padx=10)
        
        # Tạo list chứa các thứ trong tuần
        self.days = ["Thứ 2", "Thứ 3", "Thứ 4", "Thứ 5", "Thứ 6", "Thứ 7", "Chủ nhật"]
        
        # Tạo time slots
        self.create_time_slots()
        self.schedule_data = {i: {"morning": [], "afternoon": [], "evening": []} for i in range(2, 9)}  # Monday=2, Sunday=8
        
        # Nút thêm lịch thi/học
        add_button = tk.Button(self.root, text="Thêm tiết học / Lịch thi", command=self.save_schedule)
        add_button.grid(row=0, column=8, padx=10)
        
        # Hiện thị tuần chứa ngày hiện tại khi khởi động chương trình
        self.update_calendar()

    def create_time_slots(self):
        # Hàm tạo các buổi trong ngày được phân chia bằng các tiết học
        periods = ["Sáng (1-6)", "Chiều (7-12)", "Tối (13-15)"]
        for i, period in enumerate(periods):
            label = tk.Label(self.root, text=period, font=("Arial", 12), padx=10, pady=10, relief="ridge", bg="lightyellow", height=8)
            label.grid(row=i + 2, column=0, sticky="nsew")
    
    def update_calendar(self):
        for label in self.schedule_labels:
            label.destroy()
        self.schedule_labels = []
        self.day_in_weak = []
        start_of_week = self.current_date - timedelta(days=self.current_date.weekday())
        for i in range(7):
            date = start_of_week + timedelta(days=i)
            label = tk.Label(self.root, text=self.days[i] + '\n' + date.strftime("%d/%m/%Y"), font=("Arial", 10), relief="ridge")
            label.grid(row=1, column=i + 1, sticky="nsew")
            self.day_in_weak.append(label)
        
        self.date_label.config(text=f"Tuần {start_of_week.strftime('%d/%m')} - {(start_of_week + timedelta(days=6)).strftime('%d/%m')}")
        self.save_schedule()

    def show_prev_week(self):
        # Hàm tạo lệnh quay về tuần trước
        self.current_date -= timedelta(weeks=1)
        self.update_calendar()
    
    def show_next_week(self):
        # Hàm tạo lệnh quay về tuần sau
        self.current_date += timedelta(weeks=1)
        self.update_calendar()
    
    def add_schedule(self):  # Hàm thêm lịch học/thi
        self.add_window = tk.Toplevel(self.root)
        self.add_window.title("Thêm lịch học / Lịch thi")
        
        tk.Label(self.add_window, text="Môn học / Tiết học:").grid(row=0, column=0)
        self.subject_entry = tk.Entry(self.add_window)
        self.subject_entry.grid(row=0, column=1)
        
        tk.Label(self.add_window, text="Ngày (Thứ 2-7, CN = 8):").grid(row=1, column=0)
        self.day_entry = tk.Entry(self.add_window)
        self.day_entry.grid(row=1, column=1)
        
        tk.Label(self.add_window, text="Tiết học bắt đầu (1-15):").grid(row=2, column=0)
        self.periodStart_entry = tk.Entry(self.add_window)
        self.periodStart_entry.grid(row=2, column=1)
        
        tk.Label(self.add_window, text="Tiết học kết thúc (1-15):").grid(row=3, column=0)
        self.periodEnd_entry = tk.Entry(self.add_window)
        self.periodEnd_entry.grid(row=3, column=1)

        # Thêm các radioButton phục vụ chức năng phân biệt lịch thi & học
        self.thiButton = tk.Radiobutton(self.add_window, text="Lịch thi", variable=self.var, value=1)
        self.thiButton.grid(row=4, column=0)
        self.hocButton = tk.Radiobutton(self.add_window, text="Lịch học", variable=self.var, value=2)
        self.hocButton.grid(row=4, column=1)
        
        self.statusLabel = tk.Label(self.add_window, text='')
        self.statusLabel.grid(row=6, columnspan=2)

    def save_schedule(self):
        self.schedule_data = {i: {"morning": [], "afternoon": [], "evening": []} for i in range(2, 9)}
        self.cur.execute('select * from dethi')
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
                            "periodEnd": int(time[1].strftime("%H"))
                        })

                        self.display_schedule()
                        

    def display_schedule(self):
        for widget in self.root.grid_slaves():
            if int(widget.grid_info()["row"]) >= 2 and int(widget.grid_info()["column"]) >= 1:
                widget.destroy()

        # Hiển thị lịch
        for day, periods in self.schedule_data.items():
            col = day-1 # Từ T2-CN tương ứng với các cột

            for period, subjects in periods.items():
                row = 2 if period == "morning" else 3 if period == "afternoon" else 4
                for subject_info in subjects:
                    # Tạo nhãn cho mỗi môn học
                    schedule_label = tk.Label(
                        self.root,
                        text=f"Đề thi: {subject_info['subject']}\nTiết: {subject_info['periodStart']} - {subject_info['periodEnd']}",
                        font=("Arial", 10),
                        padx=5,
                        pady=5,
                        relief="ridge",
                        bg="lightpink" if self.var.get() == 1 else "lightblue"
                    )
                    # Điều chỉnh chiều cao của nhãn dựa trên số tiết học
                    period_length = subject_info["periodEnd"] - subject_info["periodStart"] + 1
                    schedule_label.grid(row=row, column=col, sticky="nsew", pady=5, ipadx=5, ipady=period_length * 10)
                    self.schedule_labels.append(schedule_label)

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("1000x600")
    app = ExamScheduler(root)
    root.mainloop()
