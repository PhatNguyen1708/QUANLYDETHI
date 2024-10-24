import cx_Oracle
from datetime import datetime


try:
	con = cx_Oracle.connect('CauHoiTracNghiem/123@localhost:1521/free')

except cx_Oracle.DatabaseError as er:
	print('There is an error in the Oracle database:', er)

else:
	try:
		cur = con.cursor()
		
		# cur.execute('INSERT INTO TAIKHOAN (ID, MATKHAU) VALUES (:id, :passWord)', {'id': id, 'passWord': passWord})
		# con.commit()

		# fetchall() is used to fetch all records from result set
		# cur.execute('select * from SinhVien')
		# rows = cur.fetchall()
		# print(rows)

		# # fetchmany(int) is used to fetch limited number of records from result set based on integer argument passed in it
		# cur.execute('select * from TAIKHOAN')
		# rows = cur.fetchmany(3)
		# print(rows)

		# fetchone() is used fetch one record from top of the result set
		mahs='HS00001'
		Class = "Hello"
		address = "rsw"
		sode = "DT00001"
		mamonhoc = "MH00003"
		# dob = input()
		# dob = datetime.strptime(dob, "%d-%m-%Y")
		# cur.execute("UPDATE SINHVIEN SET NGAYSINH = :dob WHERE MSSV = :a",{'dob': cx_Oracle.Date(dob.year, dob.month, dob.day),'a':a})
		# con.commit()
		cur.execute('select cauhoi,dapana,dapanb,dapanc,dapand from dethi, dethi_monhoc , cauhoi where dethi.madethi = dethi_monhoc.madethi  and dethi_monhoc.mamonhoc = cauhoi.mamonhoc and dethi.madethi = :madethi and dethi_monhoc.mamonhoc = : mamonhoc',{'madethi':sode,'mamonhoc':mamonhoc})
		rows = cur.fetchall()
		for data in rows:
			print(data)

	except cx_Oracle.DatabaseError as er:
		print('There is an error in the Oracle database:', er)

	except Exception as er:
		print('Error:'+str(er))

	finally:
		if cur:
			cur.close()

finally:
	if con:
		con.close()