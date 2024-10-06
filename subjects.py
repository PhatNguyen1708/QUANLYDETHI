from tkinter import *
from tkinter import messagebox
from PIL import *
import json, ast, re, string, os.path
from crawlWebtoJSON import Crawl
from Questions import Questions
from questionListView import Application

class sinhhoc:
    def __init__(self):
        super().__init__
        self.questions=Questions()
        teacherView=Tk()
        obj=Application(teacherView,r'data\sinhhoc.json')
        teacherView.mainloop()

class hoahoc:
    def __init__(self):
        super().__init__
        self.questions=Questions()
        teacherView=Tk()
        obj=Application(teacherView,r'data\hoahoc.json')
        teacherView.mainloop()

class vatly:
    def __init__(self):
        super().__init__
        self.questions=Questions()
        teacherView=Tk()
        obj=Application(teacherView,r'data\vatly.json')
        teacherView.mainloop()

class toan:
    def __init__(self):
        super().__init__
        self.questions=Questions()
        teacherView=Tk()
        obj=Application(teacherView,r'data\toan.json')
        teacherView.mainloop()

class van:
    def __init__(self):
        super().__init__
        self.questions=Questions()
        teacherView=Tk()
        obj=Application(teacherView,r'data\van.json')
        teacherView.mainloop()

class anh:
    def __init__(self):
        super().__init__
        self.questions=Questions()
        teacherView=Tk()
        obj=Application(teacherView,r'data\anh.json')
        teacherView.mainloop()

class su:
    def __init__(self):
        super().__init__
        self.questions=Questions()
        teacherView=Tk()
        obj=Application(teacherView,r'data\su.json')
        teacherView.mainloop()

class dia:
    def __init__(self):
        super().__init__
        self.questions=Questions()
        teacherView=Tk()
        obj=Application(teacherView,r'data\dia.json')
        teacherView.mainloop()

class gdcd:
    def __init__(self):
        super().__init__
        self.questions=Questions()
        teacherView=Tk()
        obj=Application(teacherView,r'data\gdcd.json')
        teacherView.mainloop()

if __name__=='__main__':
    sinhhoc()

