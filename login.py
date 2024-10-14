from tkinter import *
from tkinter import messagebox
from PIL import Image,ImageTk
import json, ast, re, string, os.path
import cx_Oracle
from DashBoard_TEACHER import *
from DashBoard_STUDENT import *

class signin:
        
    def Signin(self):
        root = Tk()
        root.title('Login')
        root.geometry('925x500+300+200')
        root.configure(bg='white')
        root.resizable(False,False)
        try:
            con = cx_Oracle.connect('CauHoiTracNghiem/123@localhost:1521/free')
        except cx_Oracle.DatabaseError as er:
            print('There is an error in the Oracle database:',er)
        cur = con.cursor()

        def signin():
            id=user.get()
            passWord=passw.get()
            cur.execute('select * from TAIKHOAN')
            data = cur.fetchall()
            try:
                accountFound=False
                for account in data:
                    if id == account[0] and passWord == cur.callfunc("f_decryptData", cx_Oracle.STRING, [account[1]]) and re.search(r'^HS',id):
                        screen=Tk()
                        cur.execute('select HOTENHS from TAIKHOAN,HOCSINH where TAIKHOAN.ID=HOCSINH.MSHS and TAIKHOAN.ID=:a',{'a':account[0]})
                        HS_name=cur.fetchall()
                        obj=dashBoard_student(screen,HS_name[0][0],account[0])
                        root.destroy()
                        screen.mainloop()
                        accountFound=True
                        return
                    elif id == account[0] and passWord == cur.callfunc("f_decryptData", cx_Oracle.STRING, [account[1]]):
                        screen=Tk()
                        cur.execute('select HOTENGV from TAIKHOAN,GIAOVIEN where TAIKHOAN.ID=GIAOVIEN.MSGV and TAIKHOAN.ID=:a',{'a':account[0]})
                        gv_name=cur.fetchall()
                        obj=dashBoard_teacher(screen,gv_name[0][0],account[0])
                        root.destroy()  
                        screen.mainloop()
                        accountFound=True
                        return
                    elif id == account[0] and passWord != cur.callfunc("f_decryptData", cx_Oracle.STRING, [account[1]]):
                        messagebox.showwarning("Wrong password",'Nhập sai mật khẩu, vui lòng nhập lại')
                        return
                if not accountFound:
                    messagebox.showwarning("Wrong ",'Tài khoản không tồn tại')
            except FileNotFoundError:
                print("Không tìm thấy file Accounts.json")                          

        def signupCommand():
                root.destroy()
                window = Tk()
                window.title('Login')
                window.geometry('925x500+300+200')
                window.configure(bg='white')
                window.resizable(False,False)
                selec_option = StringVar()

                def sign():
                    window.destroy()
                    self.Signin()

                def signup():
                    data=[]
                    id=user.get()
                    passWord=passw.get()
                    passWordConfirm=passwConfirm.get()
                    typeAccount = selec_option.get()
                    fullName=fname.get()
                    cur = con.cursor()
                    cur.execute('select * from TAIKHOAN')
                    data = cur.fetchall()

                    if id =="":
                        messagebox.showerror("Wrong ID",'Vui lòng nhập ID tài khoản')

                    for account in data:
                        if id.lower() == account[0].lower():
                            messagebox.showinfo('Failed', 'Tài Khoản đã tồn tại')
                            return
                            
                    if typeAccount == "Teacher":
                        if not re.search(r'^GV',id):
                            messagebox.showerror("Wrong ID",'Vui lòng thêm ký tự \'GV\' vào phía trước tài khoản')
                            return
                    elif typeAccount == "Student":
                        if not re.search(r'^HS',id):
                            messagebox.showerror("Wrong ID",'Vui lòng thêm ký tự \'HS\' vào phía trước tài khoản')
                            return
                    else:
                        messagebox.showwarning("Wrong type account",'Vui lòng chọn kiểu tài khoản')
                        return
                    
                    p=r'[A-Za-z0-9_#@$%&*^+=]{8,}'
                    if passWord==passWordConfirm and re.fullmatch(p,passWord): #kiểm tra mật khẩu có đúng định dạng và id có phải là một chuối 10 chữ số k
                        passWord = cur.callfunc("f_encryptData", cx_Oracle.STRING, [passWord])
                        cur.execute('INSERT INTO TAIKHOAN (ID, MATKHAU) VALUES (:id, :passWord)', {'id':  id, 'passWord': passWord})
                        if re.search(r'^HS',id):
                            cur.execute('INSERT INTO HOCSINH (MSHS, HOTENHS) VALUES (:MSHS, :HOTENHS)', {'MSHS': id, 'HOTENHS': fullName})
                        else:
                            cur.execute('INSERT INTO GIAOVIEN (MSGV, hotengv) VALUES (:MSGV, :hotengv)', {'MSGV': id, 'hotengv': fullName})
                        con.commit()
                        messagebox.showinfo('Sign up','Đăng ký thành công')
                        sign()
                    elif passWord != passWordConfirm:
                        messagebox.showerror("Wrong password",'Vui lòng nhập mật khẩu trùng khớp')
                    else:
                        messagebox.showwarning("Wrong type account",'Vui lòng kiểm tra ID (chuỗi 10 kí tự số) và chọn mật khẩu có ít nhất 8 kí tự, bao gồm các kí tự chữ hoa (A-Z), chữ thường (a-z), kí tự số (0-9) và kí tự đặc biệt')


                signup_img=r"image/signup.png"
                img_signup=ImageTk.PhotoImage(ImageTk.Image.open(signup_img).resize((400,400)))
                panel = Label(window, image = img_signup,bg='white')
                panel.place(x=50, y=50)

                frame=Frame(window,width=350,height=500,bg='white')
                frame.place(x=480,y=40)

                heading=Label(frame, text='Sign up',fg='#57a1f8',bg='white',font=('Microsoft YaHei UI Light', 23, 'bold'))
                heading.place(x=100,y=0)

                #Fullname entry
                def on_enter(e):
                    n=fname.get()
                    if n == 'Fullname':
                        fname.delete(0,'end')
                def on_leave(e):
                    n=fname.get()
                    if n == '':
                        fname.insert(0,'Fullname')
                fname = Entry(frame, width=25, fg='black', border=0, bg='white',font=('Microsoft YaHei UI Light', 11))
                fname.place(x=30,y=67)
                fname.insert(0,'Fullname')
                fname.bind('<FocusIn>',on_enter)
                fname.bind('<FocusOut>', on_leave)

                Frame(frame, width=295, height=2, bg='black').place(x=25, y=90)

                #id entry 
                def on_enter(e):
                    name=user.get()
                    if name == 'ID':
                        user.delete(0,'end')
                def on_leave(e):
                    name=user.get()
                    if name == '':
                        user.insert(0,'ID')
                user = Entry(frame, width=25, fg='black', border=0, bg='white',font=('Microsoft YaHei UI Light', 11))
                user.place(x=30,y=127)
                user.insert(0,'ID')
                user.bind('<FocusIn>',on_enter)
                user.bind('<FocusOut>', on_leave)

                Frame(frame, width=295, height=2, bg='black').place(x=25, y=150)

                # Password entry
                def on_enter(e):
                    p=passw.get()
                    if p =='Password':
                        passw.delete(0,'end')
                    passw.config(show='*')
                def on_leave(e):
                    p=passw.get()
                    if p == '':
                        passw.config(show='')
                        passw.insert(0,'Password')
                passw = Entry(frame, width=25, fg='black', border=0, bg='white',font=('Microsoft YaHei UI Light', 11))
                passw.place(x=30,y=187)
                passw.insert(0,'Password')
                passw.bind('<FocusIn>',on_enter)
                passw.bind('<FocusOut>', on_leave)

                Frame(frame, width=295, height=2, bg='black').place(x=25, y=210)

                # Confirm password entry
                def on_enter(e):
                    p=passwConfirm.get()
                    if p =='Confirm Password':
                        passwConfirm.delete(0,'end')
                    passwConfirm.config(show='*')
                def on_leave(e):
                    p=passwConfirm.get()
                    if p == '':
                        passwConfirm.config(show='')
                        passwConfirm.insert(0,'Confirm Password')
                passwConfirm = Entry(frame, width=25, fg='black', border=0, bg='white',font=('Microsoft YaHei UI Light', 11))
                passwConfirm.place(x=30,y=247)
                passwConfirm.insert(0,'Confirm Password')
                passwConfirm.bind('<FocusIn>',on_enter)
                passwConfirm.bind('<FocusOut>', on_leave)

                Frame(frame, width=295, height=2, bg='black').place(x=25, y=270)

                #Dropdown menu lựa chọn type accounts
                dropDown = OptionMenu(frame,selec_option,'Teacher','Student')
                dropDown.config(width=35, fg='black', border=0, bg='white',font=('Microsoft YaHei UI Light', 11), activebackground='white', highlightbackground='white',justify='left',textvariable=selec_option)
                dropDown['menu'].config(fg='black',bg='white',font=('Microsoft YaHei UI Light', 11))
                dropDown.place(x=30,y=305)

                Frame(frame, width=295, height=2, bg='black').place(x=25, y=330)

                #Sign up Button
                Button(frame,width=34,pady=7, text='Sign up',bg='#57a1f8',fg='white',border=0,command= signup).place(x=35,y=345)

                label=Label(frame, text="I had an account.",fg='black',bg='white',font=('Microsoft YaHei UI Light', 10))
                label.place(x=90,y=400)

                Sign_in=Button(frame,width=6,pady=7,text='Sign in', border=0, bg='white',cursor='hand2',fg='#57a1f8',font=('Microsoft YaHei UI Light', 10), activebackground='white',command=sign)
                Sign_in.place(x=200,y=392)

                window.mainloop()

        path=r"image\login.png"
        img=ImageTk.PhotoImage(ImageTk.Image.open(path).resize((400,400)))
        Label(root,image=img,bg='white',height=400,width=400).place(x=50,y=50)

        frame=Frame(root,width=350,height=350,bg='white')
        frame.place(x=480,y=70)

        heading=Label(frame, text='Sign in',fg='#57a1f8',bg='white',font=('Microsoft YaHei UI Light', 23, 'bold'))
        heading.place(x=100,y=5)

        def on_enter(e):
            name=user.get()
            if name == 'ID':
                user.delete(0,'end')
        def on_leave(e):
            name=user.get()
            if name == '':
                user.insert(0,'ID')
        user = Entry(frame, width=25, fg='black', border=0, bg='white',font=('Microsoft YaHei UI Light', 11))
        user.place(x=30,y=80)
        user.insert(0,'ID')
        user.bind('<FocusIn>',on_enter)
        user.bind('<FocusOut>', on_leave)

        Frame(frame, width=295, height=2, bg='black').place(x=25, y=107)

        # Password entry
        def on_enter(e):
            p=passw.get()
            if p =='Password':
                passw.delete(0,'end')
            passw.config(show='*')
        def on_leave(e):
            p=passw.get()
            if p =='':
                passw.config(show='')
                passw.insert(0,'Password')

        passw = Entry(frame, width=25, fg='black', border=0, bg='white',font=('Microsoft YaHei UI Light', 11))
        passw.place(x=30,y=150)
        passw.insert(0,'Password')
        passw.bind('<FocusIn>',on_enter)
        passw.bind('<FocusOut>', on_leave)

        Frame(frame, width=295, height=2, bg='black').place(x=25, y=177)

        Button(frame,width=34,pady=7, text='Sign in',bg='#57a1f8',fg='white',border=0,command=signin).place(x=35,y=204)
        label=Label(frame, text="Don't have account?",fg='black',bg='white',font=('Microsoft YaHei UI Light', 10))
        label.place(x=75,y=270)

        Sign_up=Button(frame,width=6,pady=7,text='Sign up', border=0, bg='white',cursor='hand2',fg='#57a1f8',font=('Microsoft YaHei UI Light', 10), activebackground='white', command= signupCommand)
        Sign_up.place(x=208,y=262)
        root.mainloop()

if __name__=="__main__":
    a=signin()
    a.Signin()