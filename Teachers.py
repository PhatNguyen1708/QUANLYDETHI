from Questions import *
from tkinter import messagebox

class Teacher(Questions):
    def __init__(self,subject_code):
        super().__init__()
        self.subject_code = subject_code
        
    def add_question_file(self):
        if self.subject_code:
            super().getQues(self.subject_code)
        else:
            print("Mã môn học không tồn tại!")

    def Create(self,question, options, answer,filepath):
        question_data = {
                "question": question,
                "option": options,
                "answer": answer
        }
        self.questions.append(question_data)
        super().save_question(filepath)
        messagebox.showinfo("Successful",f"Dữ liệu đã được ghi vào file '{filepath}' thành công.")

    def edit(self,filepath,index,replace):
        if 0 <= index-1 < len(self.questions):
            self.questions[index-1]=replace
        super().save_question(filepath)

    def remove(self,filepath,index):
        if 0 <= index-1 < len(self.questions):
            self.questions.remove(self.questions[index-1])
        super().save_question(filepath)




