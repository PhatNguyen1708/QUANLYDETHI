import tkinter as tk

def hien_thi():
    global labels
    # Tạo và hiển thị các Label
    for i in range(1):  # Ví dụ tạo 5 Label
        label = tk.Label(root, text=f"Label {i + 1}")
        label.pack()
        labels.append(label)

def xoa_labels():
    # Xóa tất cả Label
    global labels
    for label in labels:
        label.destroy()
    labels = []  # Làm trống danh sách labels

# Tạo cửa sổ chính
root = tk.Tk()
root.title("Hiển Thị và Xóa Label")
root.geometry("300x200")

# Danh sách lưu các label đã tạo
labels = []

# Tạo các nút
btn_hien_thi = tk.Button(root, text="Hiển Thị", command=hien_thi)
btn_hien_thi.pack(pady=10)

btn_xoa = tk.Button(root, text="Xóa", command=xoa_labels)
btn_xoa.pack(pady=10)

# Chạy ứng dụng
root.mainloop()
