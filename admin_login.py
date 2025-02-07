import tkinter as tk
from tkinter import ttk, messagebox
import cx_Oracle
import datetime

# Database connection
class Database:
    def __init__(self):
        self.connection = cx_Oracle.connect("CauHoiTracNghiem/123@localhost:1521/free")
        self.cursor = self.connection.cursor()

    def execute_query(self, query, params=None):
        if params is None:
            params = []
        self.cursor.execute(query, params)
        self.connection.commit()

    def fetch_query(self, query, params=None):
        if params is None:
            params = []
        self.cursor.execute(query, params)
        return self.cursor.fetchall()

    def close(self):
        self.cursor.close()
        self.connection.close()

# Main Application Class
class ExamApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Exam Management System")
        self.root.geometry("800x600")
        
        self.db = Database()
        
        self.setup_ui()

    def setup_ui(self):
        # Tabs
        self.tab_control = ttk.Notebook(self.root)

        self.question_tab = ttk.Frame(self.tab_control)
        self.test_tab = ttk.Frame(self.tab_control)
        self.schedule_tab = ttk.Frame(self.tab_control)
        self.audit_tab = ttk.Frame(self.tab_control)

        # self.tab_control.add(self.question_tab, text="Manage Questions")
        # self.tab_control.add(self.test_tab, text="Take Test")
        # self.tab_control.add(self.schedule_tab, text="Exam Schedule")
        self.tab_control.add(self.audit_tab, text="Audit Logs")

        self.tab_control.pack(expand=1, fill="both")

        # Setup individual tabs
        self.setup_question_tab()
        self.setup_test_tab()
        self.setup_schedule_tab()
        self.setup_audit_tab()

    def setup_question_tab(self):
        # Manage Questions
        pass

    def setup_test_tab(self):
        # Take Test
        pass

    def setup_schedule_tab(self):
        # Create Exam Schedule
        pass

    def create_schedule(self):
        pass

    def setup_audit_tab(self):
        # View Audit Logs
        self.audit_tree = ttk.Treeview(self.audit_tab, columns=("ID", "Time", "User", "Action", "Table", "Details"), show="headings")

        self.audit_tree.heading("ID", text="ID")
        self.audit_tree.heading("Time", text="Action Time")
        self.audit_tree.heading("User", text="User ID")
        self.audit_tree.heading("Action", text="Action Type")
        self.audit_tree.heading("Table", text="Table Name")
        self.audit_tree.heading("Details", text="Details")

        self.audit_tree.column("ID", width=50)
        self.audit_tree.column("Time", width=150)
        self.audit_tree.column("User", width=100)
        self.audit_tree.column("Action", width=100)
        self.audit_tree.column("Table", width=100)
        self.audit_tree.column("Details", width=250)

        self.audit_tree.pack(fill="both", expand=True)

        tk.Button(self.audit_tab, text="Refresh Logs", command=self.refresh_audit_logs).pack(pady=10)

    def refresh_audit_logs(self):
        for row in self.audit_tree.get_children():
            self.audit_tree.delete(row)

        query = "SELECT logID, actionTime, ID, actionType, tableName, details FROM audit_log ORDER BY actionTime DESC"
        logs = self.db.fetch_query(query)

        for log in logs:
            self.audit_tree.insert("", "end", values=log)

    def close_app(self):
        self.db.close()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = ExamApp(root)
    root.protocol("WM_DELETE_WINDOW", app.close_app)
    root.mainloop()
