from datetime import datetime, timedelta

# Thời gian cụ thể
specific_time = datetime(2024, 12, 3, 21, 40)

current_time = datetime.now()

# So sánh thời gian
if current_time < specific_time:
    print("Chưa tới giờ")
elif current_time > specific_time and int((current_time - specific_time).total_seconds() // 60) > 10:
    print("Trễ Giờ")
elif current_time > specific_time:
    minutes_late = int((current_time - specific_time).total_seconds() // 60)
    print(f"trễ {minutes_late} phút ")
else:
    print("đúng đúng")
