import tkinter as tk

def on_select():
    selected = var.get()
    print(f"Bạn đã chọn: {selected}")

# Tạo cửa sổ
root = tk.Tk()
root.title("Check Box Hình Tròn")
root.geometry("300x200")

# Tạo biến để lưu giá trị
var = tk.StringVar(value="")

# Tạo Radiobutton (mô phỏng check box hình tròn)
tk.Radiobutton(root, text="Lựa chọn 1", value="Lựa chọn 1").pack(anchor="w", padx=10, pady=5)
tk.Radiobutton(root, text="Lựa chọn 2", value="Lựa chọn 2").pack(anchor="w", padx=10, pady=5)
tk.Radiobutton(root, text="Lựa chọn 3", value="Lựa chọn 3").pack(anchor="w", padx=10, pady=5)

# Chạy ứng dụng
root.mainloop()
