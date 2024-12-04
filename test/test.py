from datetime import datetime, timedelta


current_time = datetime.now()

print(current_time.strftime("%d/%m/%Y")+' '+current_time.strftime("%H:%M"))
