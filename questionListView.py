import json
from tkinter import messagebox, ttk
from Questions import *
from Teachers import *
from tkinter import *

class Application:
    def __init__(self,teacherView):
        super().__init__()
        self.teacherView=teacherView
        self.questions = Questions()
        self.teacher = Teacher()

        #### khởi tạo window
        self.teacherView.title("Quiz Management System")
        self.teacherView.geometry('925x440+300+200')
        self.teacherView.config(bg='white')
        
        titleTable=Label(self.teacherView,text="List câu hỏi trắc nghiệm",bg='white',fg='#57a1f8', font=('Arial', 20, 'bold')).place(x=310,y=10)

        #### khởi tạo các nút chức năng
        self.create_button = Button(self.teacherView, text="Create", command=self.create_question, fg='white',bg='#57a1f8',border=0, font=('Microsoft YaHei UI Light', 13, 'bold'))
        self.create_button.place(x=20,y=360,width=160,height=40)
        self.edit_button = Button(self.teacherView, text="Update", command=self.edit_question, fg='white',bg='#57a1f8',border=0, font=('Microsoft YaHei UI Light', 13, 'bold'))
        self.edit_button.place(x=200,y=360,width=160,height=40)
        self.remove_button = Button(self.teacherView, text="Delete", command=self.remove_question, fg='white',bg='#57a1f8',border=0, font=('Microsoft YaHei UI Light', 13, 'bold'))
        self.remove_button.place(x=380,y=360,width=160,height=40)
        self.createWeb_button = Button(self.teacherView, text="Create from web", command=self.creat_fromWeb, fg='white',bg='#57a1f8',border=0, font=('Microsoft YaHei UI Light', 13, 'bold'))
        self.createWeb_button.place(x=560,y=360,width=160,height=40)

        self.refreshButton = Button(self.teacherView, text="Refresh", command=self.refreshTabel, fg='white',bg='#57a1f8',border=0, font=('Microsoft YaHei UI Light', 13, 'bold'))
        self.refreshButton.place(x=740,y=360,width=160,height=40)
        #### Tạo giao diện bảng và thanh lăn
        scrolly = Scrollbar(self.teacherView, orient="vertical")
        scrollx = Scrollbar(self.teacherView, orient="horizontal")

        self.tree = ttk.Treeview(self.teacherView, columns=("MACAUHOI", "CAUHOI", "DAPANA","DAPANB","DAPANC","DAPAND", "DAPAN_DUNG"), yscrollcommand = scrolly.set, xscrollcommand=scrollx.set)

        scrollx.place(x=20,y=330, width=880)
        scrolly.place(x=900,y=50,height=280)
        
        scrollx.config(command=self.tree.xview)
        scrolly.config(command=self.tree.yview)

        self.tree.heading("#0", text="ID")
        self.tree.column("#0",width=45,anchor='nw')
        self.tree.heading("MACAUHOI", text="MACAUHOI")
        self.tree.heading("CAUHOI", text="Question")
        self.tree.heading("DAPANA", text="A")
        self.tree.heading("DAPANB", text="B")
        self.tree.heading("DAPANC", text="C")
        self.tree.heading("DAPAND", text="D")
        self.tree.heading("DAPAN_DUNG", text="Answer")
        self.tree.column("DAPAN_DUNG",width=60,anchor='nw')
        self.tree.place(x=20,y=50,width=880,height=280)

        self.load_questions()
        self.display_questions()
        
        # self.countLabel=Label(self.teacherView,text=f"Tổng câu hỏi trong môn học này: " + str(self.count_question()),bg='white',font=('Arial', 13, 'italic'))
        # self.countLabel.place(x=10,y=410)

    def load_questions(self):
        self.teacher.add_question_file()
        
    def create_question(self):
        create_window = Toplevel(self.teacherView)
        create_window.title("Create Question")
        create_window.geometry('450x300+550+350')
        create_window.config(background='white')

        question_label = Label(create_window, text="Question: ",bg='white',fg='black', font=('Arial', 13)).place(x=20,y=20)
        question_entry = Entry(create_window,width=35, fg='black', border=0, bg='white',font=('Arial', 13))
        question_entry.place(x=100,y=22)
        # question_entry.insert(0,'Nhập câu hỏi')
        Frame(create_window, width=310, height=2, bg='black',border=0).place(x=100,y=45)

        options_label = Label(create_window, text="Options:",bg='white',fg='black', font=('Arial', 13)).place(x=20,y=60)
        options_entry = Entry(create_window,width=35, fg='black', border=0, bg='white',font=('Arial', 13))
        options_entry.place(x=100,y=62)
        # options_entry.insert(0,'Nhập lựa chọn, ngăn cách bằng dấu phẩy')
        Frame(create_window, width=310, height=2, bg='black',border=0).place(x=100,y=85)

        answer_label = Label(create_window, text="Answer:",bg='white',fg='black', font=('Arial', 13)).place(x=20,y=100)
        answer_entry = Entry(create_window,width=35, fg='black', border=0, bg='white',font=('Arial', 13))
        answer_entry.place(x=100,y=102)
        answer_entry.insert(0,'Nhập câu trả lời đúng (0,1,2,3)')
        Frame(create_window, width=310, height=2, bg='black',border=0).place(x=100,y=125)


        def create():
            question = question_entry.get()
            options = options_entry.get().split(',')
            answer = answer_entry.get()
            if question == '' or options == '' or answer == '':
                messagebox.showwarning('Lỗi','Vui lòng nhập lại và điền đầy đủ thông tin')
            else:
                self.teacher.Create(question, options, int(answer), self.jsonFilePath)
                create_window.destroy()
                self.display_questions()
                self.countLabel.config(text=f"Tổng câu hỏi trong môn học này: " + str(self.count_question()))

        create_button = Button(create_window, text="Create", command=create, fg='white',bg='#57a1f8',border=0, font=('Microsoft YaHei UI Light', 13, 'bold')).place(x=150,y=145,width=160,height=40)

    def edit_question(self):
        edit_window = Toplevel(self.teacherView)
        edit_window.title("Edit Question")
        edit_window.geometry('450x300+550+350')
        edit_window.config(background='white')

        index_label = Label(edit_window, text="Index:",bg='white',fg='black', font=('Arial', 13)).place(x=20,y=20)
        index_entry = Entry(edit_window,width=35, fg='black', border=0, bg='white',font=('Arial', 13))
        index_entry.place(x=100,y=22)
        index_entry.insert(0,'Nhập số thứ tự câu muốn sửa')
        Frame(edit_window, width=310, height=2, bg='black',border=0).place(x=100,y=45)

        question_label = Label(edit_window, text="Question:",bg='white',fg='black', font=('Arial', 13)).place(x=20,y=60)
        question_entry = Entry(edit_window,width=35, fg='black', border=0, bg='white',font=('Arial', 13))
        question_entry.place(x=100,y=62)
        question_entry.insert(0,'Nhập câu hỏi')
        Frame(edit_window, width=310, height=2, bg='black',border=0).place(x=100,y=85)

        options_label = Label(edit_window, text="Options:",bg='white',fg='black', font=('Arial', 13)).place(x=20,y=100)
        options_entry = Entry(edit_window,width=35, fg='black', border=0, bg='white',font=('Arial', 13))
        options_entry.place(x=100,y=102)
        options_entry.insert(0,'Nhập lựa chọn, ngăn cách bằng dấu phẩy')
        Frame(edit_window, width=310, height=2, bg='black',border=0).place(x=100,y=125)

        answer_label = Label(edit_window, text="Answer:",bg='white',fg='black', font=('Arial', 13)).place(x=20,y=140)
        answer_entry = Entry(edit_window,width=35, fg='black', border=0, bg='white',font=('Arial', 13))
        answer_entry.place(x=100,y=142)
        answer_entry.insert(0,'Nhập câu trả lời đúng (0,2,3,4)')
        Frame(edit_window, width=310, height=2, bg='black',border=0).place(x=100,y=165)

        def edit():
            index = index_entry.get()
            question = question_entry.get()
            options = options_entry.get().split(',')
            answer = answer_entry.get()
            if question == '' or options == '' or answer == '' or index == '':
                messagebox.showwarning('Lỗi','Vui lòng nhập lại và điền đầy đủ thông tin')
            else:
                self.teacher.edit(self.jsonFilePath,int(index), {"question": question, "option": options, "answer": int(answer)})
                edit_window.destroy()
                self.display_questions()
                self.countLabel.config(text=f"Tổng câu hỏi trong môn học này: " + str(self.count_question()))


        edit_button = Button(edit_window, text="Update", command=edit, fg='white',bg='#57a1f8',border=0, font=('Microsoft YaHei UI Light', 13, 'bold')).place(x=150,y=185,width=160,height=40)

    def remove_question(self):
        remove_window = Toplevel(self.teacherView)
        remove_window.title("Remove Question")
        remove_window.geometry('450x200+550+350')
        remove_window.config(background='white')

        index_label = Label(remove_window, text="Index:",bg='white',fg='black', font=('Arial', 13)).place(x=20,y=20)
        index_entry = Entry(remove_window,width=35, fg='black', border=0, bg='white',font=('Arial', 13))
        index_entry.place(x=100,y=22)
        index_entry.insert(0,'Nhập số thứ tự câu muốn xóa')
        Frame(remove_window, width=310, height=2, bg='black',border=0).place(x=100,y=45)

        def remove():
            index = index_entry.get()
            if index == '':
                messagebox.showwarning('Lỗi','Vui lòng nhập lại và điền đầy đủ thông tin')
            else:
                self.teacher.remove(self.jsonFilePath,int(index))
                remove_window.destroy()
                self.display_questions()
                self.countLabel.config(text=f"Tổng câu hỏi trong môn học này: " + str(self.count_question()))

        remove_button = Button(remove_window, text="Remove", command=remove, fg='white',bg='#57a1f8',border=0, font=('Microsoft YaHei UI Light', 13, 'bold')).place(x=150,y=65,width=160,height=40)

    def creat_fromWeb(self):
        windowCreatWeb=Toplevel(self.teacherView)
        windowCreatWeb.title("Get questions from web")
        windowCreatWeb.geometry('450x300+550+350')
        windowCreatWeb.config(background='white')
        inserLinkLabel=Label(windowCreatWeb,text='Link website: ',bg='white',fg='black', font=('Arial', 13)).place(x=20,y=20)
        inserLinkEntry=Entry(windowCreatWeb,width=35, fg='black', border=0, bg='white',font=('Arial', 13))
        inserLinkEntry.place(x=120,y=22)
        inserLinkEntry.insert(0,'Nhập link website muốn lấy đề')
        Frame(windowCreatWeb, width=310, height=2, bg='black',border=0).place(x=120,y=45)

        def creatWeb():
            url=inserLinkEntry.get()
            if url == '':
                messagebox.showwarning('Lỗi','Vui lòng nhập lại và điền đầy đủ thông tin')
            else:
                self.questions.getQues(url,r'data\webData.txt',self.jsonFilePath)
                windowCreatWeb.destroy()
                self.display_questions()
                self.countLabel.config(text=f"Tổng câu hỏi trong môn học này: " + str(self.count_question()))

        creatWeb_button = Button(windowCreatWeb, text="Create", command=creatWeb, fg='white',bg='#57a1f8',border=0, font=('Microsoft YaHei UI Light', 13, 'bold')).place(x=150,y=65,width=160,height=40)

    def display_questions(self):
        self.tree.delete(*self.tree.get_children())
        for idx, question in enumerate(self.teacher.questions, 1):
            print(question)
            id,question_text, A,B,C,D,answer = self.teacher.display_question(idx-1)
            self.tree.insert("", "end", text=str(idx), values=(id,question_text,A,B,C,D,answer))

    def count_question(self):
        return self.questions.count_ques()
    
    def refreshTabel(self):
        self.tree.delete(*self.tree.get_children())
        self.display_questions()
        self.countLabel.config(text=f"Tổng câu hỏi trong môn học này: " + str(self.count_question()))


if __name__ == "__main__":
    teacherView=Tk()
    obj = Application(teacherView)
    teacherView.mainloop()




