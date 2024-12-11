import tkinter as tk
from tkinter import messagebox, simpledialog
import json, random, datetime
import cx_Oracle

class QuizApp: 
    def __init__(self, window,soDe,mamonhoc,id,passwd,later):

        self.id=id
        self.passwd = passwd
        self.soDe=soDe
        self.mamonhoc=mamonhoc
        self.time = (15*60) - (later*60)
        self.time_can_finish = (15*60)/3

        try:
            self.con = cx_Oracle.connect(f'{self.id}/{self.passwd}@localhost:1521/free')
        except cx_Oracle.DatabaseError as er:
            print('There is an error in the Oracle database:',er)
        self.cur = self.con.cursor()

        self.window = window
        self.window.title("Bài tập Multiple Choice")
        self.window.geometry('925x520+300+200')
        self.window.config(bg='white')
        self.window.protocol("WM_DELETE_WINDOW", self.on_close)
#------------------------ KHỞI TẠO CÁC KHUNG VÀ CHÈN CÂU HỎI, ĐÁP ÁN
        self.questions = list(self.load_questions_from_file(self.soDe,self.mamonhoc))
        self.questions = self.shuffle_subarray(self.questions,0,len(self.questions)-1)# RANDOM CÂU HỎI NÈ
    
        self.num_questions = min(len(self.questions), 10)
        self.current_question_index = 0
        self.answers = [-1] * self.num_questions  #khởi tạo giá trị mặc định là -1 cho những câu hỏi chưa chọn đáp án

        self.clock = tk.Label(self.window, text="00:00:00", font=("Courier", 20), width=10,bg='white')
        self.clock.pack(padx=10)

        self.timer()

        self.question_label = tk.Label(self.window, text="", wraplength=750, font=('Arial', 18), bg='white')
        self.question_label.pack(pady=10)

        self.option_buttons = []
        self.selected_color = "#64a587"  # Màu nền khi được chọn
        self.default_color = self.window.cget("bg")  # Màu nền mặc định của cửa sổ
        for i in range(4):
            button = tk.Button(self.window, text="", command=lambda idx=i: self.save_answer(idx),font=('Arial', 15), fg='black', bg='gray', width=78, bd=2,wraplength=750)
            self.option_buttons.append(button)
            button.place(x=30, y=i * 75 + 150)

        self.count_label = tk.Label(self.window, text="")
        self.count_label.place(x=435, y=490)

        self.next_button = tk.Button(self.window, text="Tiếp theo", command=self.next_question,font=('Arial', 18), bg='white', activebackground='#64a587', width=8)
        self.next_button.place(x=680, y=440)

        self.prev_button = tk.Button(self.window, text="Quay lại", command=self.prev_question,font=('Arial', 18), bg='white', activebackground='#64a587', width=8)
        self.prev_button.place(x=130, y=440)

        self.finish_button = tk.Button(self.window, text="Nộp bài", command=self.finish_quiz,font=('Arial', 18), bg='white', activebackground='#64a587', width=8)
        self.finish_button.place(x=405, y=440)

        self.update_count_label()
        self.load_question(self.current_question_index)

    def timer(self):
        if self.time <= 0:
            self.clock.configure(text="00:00:00")
            for i in range(len(self.answers)):
                if self.answers[i] == -1:
                    self.answers[i] = 1000000
            messagebox.showinfo("Thông báo", "Hết Thời Gian Làm Bài")
            self.finish_quiz()
        else:
            hours = self.time // 3600
            mins = (self.time // 60) % 60
            secs = self.time % 60
            self.clock.configure(text="{:02d}:{:02d}:{:02d}".format(hours,mins,secs))
            self.time -= 1
            self.window.after(1000, self.timer)

    def shuffle_subarray(self,arr, start, end):
        if start < 0 or end >= len(arr) or start > end:
            raise ValueError("Chỉ số không hợp lệ")
        
        subarray = arr[start:end+1]
        
        random.shuffle(subarray)

        arr[start:end+1] = subarray
        
        return arr

    def load_questions_from_file(self,sode,mamonhoc):
        self.cur.execute('select cauhoi,dapana,dapanb,dapanc,dapand,DAPAN_DUNG from CauHoiTracNghiem.dethi, CauHoiTracNghiem.dethi_monhoc , CauHoiTracNghiem.cauhoi where dethi.madethi = dethi_monhoc.madethi  and dethi_monhoc.mamonhoc = cauhoi.mamonhoc and dethi.madethi = :madethi and dethi_monhoc.mamonhoc = : mamonhoc',{'madethi':sode,'mamonhoc':mamonhoc})
        data = self.cur.fetchall()
        return data

    def load_question(self, index):
        question_data = self.questions[index] #lấy dữ liệu câu hỏi từ index được truyền vào
        self.question_label.config(text=question_data[0]) #chèn câu hỏi vào label
        
        for i in range(1,len(question_data)-1):
            self.option_buttons[i-1].config(text=question_data[i], bg=self.default_color) #chèn 4 lựa chọn và màu bg mặc định là màu cửa sổ

        selected_index = self.answers[index] #lấy dữ liệu của đáp án (0,1,2,3)
        if selected_index != -1: #nếu lựa chọn nào được chọn thì nó sẽ đổi màu ô đó
            self.option_buttons[selected_index].config(bg=self.selected_color) 

    def update_count_label(self): #hiển thị vị trí của câu hỏi hiện tại trên tổng số câu (vị trí con trỏ +1)/(tổng số câu)
        count_text = f"{self.current_question_index + 1}/{self.num_questions}"
        self.count_label.config(text=count_text, font=('Arial', 18), bg='white')

    def save_answer(self, idx):
        self.answers[self.current_question_index] = idx
        for i in range(len(self.option_buttons)):
            if i != idx:
                self.option_buttons[i].config(bg=self.default_color)
        # Đổi màu lựa chọn
        self.option_buttons[idx].config(bg=self.selected_color)

    def next_question(self):
        if self.current_question_index < self.num_questions - 1:
            self.current_question_index += 1
            self.update_count_label()
            self.load_question(self.current_question_index)
        else:
            messagebox.showinfo("Thông báo", "Đã đến câu hỏi cuối cùng.")

    def prev_question(self):
        if self.current_question_index > 0:
            self.current_question_index -= 1
            self.update_count_label()
            self.load_question(self.current_question_index)
        else:
            messagebox.showinfo("Thông báo", "Đã đến câu hỏi đầu tiên.")

    def finish_quiz(self):
        if self.time > self.time_can_finish:
            messagebox.showwarning("Cảnh báo", "Chưa hết giờ làm bài")
            return
        def decrypt_answer(data):
            return self.cur.callfunc("CauHoiTracNghiem.CRYPTO.RSA_DECRYPT", cx_Oracle.STRING, [data,'MIICdwIBADANBgkqhkiG9w0BAQEFAASCAmEwggJdAgEAAoGBAJ5q60k+f23pXk1ydy5fsMdl0b6P8eV+X1q73CaSOTVO/znN/wWCZIqaeX/u9fn/4anytsFqZYRMNfVqTKR7IqtLi65jAVrgg+CW/MAYZ4vB3o3rW4hlNvv2cMQJN/3n/2i3YN6moVvNmuThqhVHy8s8L+N25BxPsQWaRXXdmetXAgMBAAECgYBjhQGossV08/1VJAqxLFYu/c0FLQKmzHv00T2dUZD051q5IqsJ9/9Xf3HCqAkI8/H9RMgAu+lockQXl57sWZrOBDLCFsNP32Q3FJC6iSILv+QKq9g5xa0SZgy0i/s9jQeqcgjIaX/eM30/hct02qBWSxjvrrYDdKFkzMa6GXe3MQJBAPvvp5zhsRNSgB1oyc5AZNDfpahtWlTKKvQ4uBp9SaT0rXZVXW026pYIyT7ICzh/cseYPQU4TOAmx34P1g1vXLkCQQCg+RbJxWlnZElh+2KKBTJO6DIc66uWP8kS439HHnsHrxAuU9K9dw3dOIm80Xh4wo/izFlMxPYAc2H32YfcPiCPAkEA2eVbCHrC1j1ihQ0ejX5wM59a/aMmn3MDV5q+0FpQGZVteY03csAugHk05VHLMqA4O5zWGe+pvayMmeFEdvY8MQJBAJm/0Gg/ygEa5IxVkzTI6dg8J0FAR89mdSM5b2P6VQBt0UKuhWa5w+A8FDLoz+xnyQ6Sp+iPZ3fevQACIaXXITkCQBsFfjhKTH875WHKDD7oKFdkfo6kZV3E7OQ0c3jdsZDmBm1doPLPlHKjpd39YeNklGcK2LNDnaLerI7t2iQi52Q='])
        if -1 in self.answers: #nếu vẫn còn câu chưa làm
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn đáp án cho tất cả các câu hỏi.")
            return

        correct_answers = sum(1 for user_ans, correct_ans in zip(self.answers, [decrypt_answer(q[5]) for q in self.questions]) if user_ans == int(correct_ans))
        score = round(correct_answers / self.num_questions * 10, 2)
        
        current_time = datetime.datetime.now()

        self.cur.execute('ALTER SESSION SET NLS_TIMESTAMP_FORMAT = "DD-MM-YYYY HH24:MI:SS"')
        self.cur.execute('''insert into CauHoiTracNghiem.KETQUA (MSHS,MAMONHOC,MADETHI,DIEMTHI,THOIGIAN_HOANTHANH)
                        values (:MSHS,:MAMONHOC,:MADETHI,:DIEMTHI,:THOIGIAN_HOANTHANH)''',
                        {'MSHS':self.id,'MAMONHOC':self.mamonhoc,'MADETHI':self.soDe,'DIEMTHI':int(score),'THOIGIAN_HOANTHANH':current_time.strftime("%d/%m/%Y")+' '+current_time.strftime("%H:%M")})
        self.con.commit()

        messagebox.showinfo("Thông báo", f"Điểm của bạn là: {score}. Kết quả đã được lưu vào kết quả học tập\n Mã số học sinh: {self.id}.")
        self.window.destroy()
        from DashBoard_STUDENT import dashBoard_student
        studentView = tk.Tk()
        self.con.close()
        obj = dashBoard_student(studentView,None,self.id,self.passwd)
        studentView.mainloop()
    def on_close(self):
        self.finish_quiz()

if __name__ == "__main__":
    root = tk.Tk()
    app = QuizApp(root,"DT00001","MH00001",'HS00001',123,14)
    root.mainloop()
