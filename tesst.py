import cx_Oracle


try:
	con = cx_Oracle.connect('QLTracNghiem/123@localhost:1521/free')

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
		a='HV00001'
		cur.execute('select * from SINHVIEN where MSSV=:a',{'a':a})
		rows = cur.fetchall()
		print(rows[0][4])

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