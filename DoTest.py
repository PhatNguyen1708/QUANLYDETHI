import tkinter as tk
from tkinter import messagebox, simpledialog
import json, random, datetime

class QuizApp:
    def __init__(self, window, filepath, soDe, subject,id):
        self.filepath = filepath
        self.id=id
        self.soDe=soDe
        self.subject=subject
        self.window = window
        self.window.title("Bài tập Multiple Choice")
        self.window.geometry('925x520+300+200')
        self.window.config(bg='white')
#------------------------ KHỞI TẠO CÁC KHUNG VÀ CHÈN CÂU HỎI, ĐÁP ÁN

        self.questions = self.load_questions_from_file(filepath, soDe)
        self.num_questions = min(len(self.questions), 10)
        self.current_question_index = 0
        self.answers = [-1] * self.num_questions  #khởi tạo giá trị mặc định là -1 cho những câu hỏi chưa chọn đáp án

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

    def load_questions_from_file(self, filepath, soDe):
        with open(filepath, 'r', encoding='utf-8') as file:
            data = json.load(file)
        start_index = soDe * 10 
        end_index = start_index + 10 #lấy 10 câu bắt đầu từ vị trí soDe*10
        return data[start_index:end_index]

    def load_question(self, index):
        question_data = self.questions[index] #lấy dữ liệu câu hỏi từ index được truyền vào
        self.question_label.config(text=question_data['question']) #chèn câu hỏi vào label
        options = question_data['option'] 
        for i, option in enumerate(options): 
            self.option_buttons[i].config(text=option, bg=self.default_color) #chèn 4 lựa chọn và màu bg mặc định là màu cửa sổ

        selected_index = self.answers[index] #lấy dữ liệu của đáp án (0,1,2,3)
        if selected_index != -1: #nếu lựa chọn nào được chọn thì nó sẽ đổi màu ô đó
            self.option_buttons[selected_index].config(bg=self.selected_color) 

    def update_count_label(self): #hiển thị vị trí của câu hỏi hiện tại trên tổng số câu (vị trí con trỏ +1)/(tổng số câu)
        count_text = f"{self.current_question_index + 1}/{self.num_questions}"
        self.count_label.config(text=count_text, font=('Arial', 18), bg='white')

    def save_answer(self, idx):
        self.answers[self.current_question_index] = idx
        # Đổi màu lại như cũ nếu chuyển sang câu kế tiếp
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
        if -1 in self.answers: #nếu vẫn còn câu chưa làm
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn đáp án cho tất cả các câu hỏi.")
            return

        correct_answers = sum(1 for user_ans, correct_ans in zip(self.answers, [q['answer'] for q in self.questions]) if user_ans == correct_ans)
        score = round(correct_answers / self.num_questions * 10, 2)
        
        result = {
            "score": score,
            "subject": self.subject,
            "soDe": self.soDe,  # Thêm số đề vào kết quả
            "time_completed": str(datetime.datetime.now())
        }

        accounts_file = r'data\Accounts.json'
        try:
            with open(accounts_file, 'r', encoding='utf-8') as file:
                accounts_data = json.load(file)
        except FileNotFoundError:
            accounts_data = []

        user_exists = False        # Kiểm tra nếu người dùng đã tồn tại trong danh sách tài khoản
        for account in accounts_data:
            if account['id'] == self.id:
                if 'quizzes' not in account:
                    account['quizzes'] = []  # Tạo một danh sách mới nếu 'quizzes' không tồn tại
                account['quizzes'].append(result)
                user_exists = True
                break
        with open(accounts_file, 'w', encoding='utf-8') as file:
            json.dump(accounts_data, file, ensure_ascii=False)

        messagebox.showinfo("Thông báo", f"Điểm của bạn là: {score}. Kết quả đã được lưu vào kết quả học tập\n Mã số học sinh: {self.id}.")
        self.window.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = QuizApp(root, r'data\sinhhoc.json', 1, "sinh học",'2033225436')
    root.mainloop()