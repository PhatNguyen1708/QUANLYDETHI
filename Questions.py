from base64 import encode
from email.charset import Charset
import json
from os import name
import string
from crawlWebtoJSON import Crawl


class Questions():
    def __init__(self):
        self.questions=[]

    def getQues(self,url,filepath,jsonFilePath):
        a=Crawl(url)
        a.getCrawlWebData(filepath)
        a.clearWebData(filepath)
        a.clearQuestionsData(filepath)
        a.saveQuestionsData(filepath,jsonFilePath)
    
    def add_fileJson(self,jsonFilePath):
        file=open(jsonFilePath,"r",encoding='utf-8')
        y=json.load(file)
        for i in y:
            self.questions.append(i)

    def save_question(self,jsonFilePath):
        with open(jsonFilePath, 'w',encoding='utf-8') as file:
            json.dump(self.questions,file, indent=4)

    def display_question(self, index):
            if 0 <= index < len(self.questions):
                question_data = self.questions[index]
                question_text = question_data["question"]
                options = (question_data["option"])
                A=options[0]
                B=options[1]
                C=options[2]
                D=options[3]
                answer = chr(65 + question_data["answer"])
                return question_text,A,B,C,D, answer
            else:
                return "Invalid question index."

    def count_ques(self, jsonFilePath):
        count = 0
        try:
            with open(jsonFilePath, 'r', encoding='utf-8') as f:
                data = json.load(f)
                count = len(data)  # Số lượng câu hỏi chính là số lượng phần tử trong danh sách data
            return count
        except FileNotFoundError:
            messagebox.showerror("Error", "File not found.")
        except json.JSONDecodeError:
            messagebox.showerror("Error", "Invalid JSON format.")





        
    




