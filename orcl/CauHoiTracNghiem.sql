 
--TẠO BẢNG
CREATE TABLE HOCSINH    
(
    MSHS varchar2(12) NOT NULL,
    HOTENHS nvarchar2(50),
    NGAYSINH date,
    GIOITINH nvarchar2(10),
    DIACHI nvarchar2(100),
    LOP nvarchar2(20)
)
/
create table TAIKHOAN
(
    ID varchar2(12) not null,
    MATKHAU NVARCHAR2(2000)
)
/
create table GIAOVIEN
(
    MSGV varchar(12),
    HOTENGV nvarchar2(50),
    NGAYSINH date,
    GIOITINH nvarchar2(10),
    MAMONHOC VARCHAR2(12)
)

 
/
create table MONHOC
(
    MAMONHOC varchar2(12),
    TENMONHOC nvarchar2(50)
)
/
create table DETHI
(
    MADETHI varchar2(12),
    SOCAUHOI int
)
/
CREATE TABLE DETHI_MONHOC
(
    MADETHI varchar2(12),
    MAMONHOC varchar2(12),
    THOIGIAN_BATDAU TIMESTAMP --TIMESTAMP LƯU TRỮ THÔNG TIN GIỜ&NGÀY THÁNG NĂM
)
/
create table CAUHOI
(
    MAMONHOC varchar2(12),
    MACAUHOI varchar2(12),
    CAUHOI NVARCHAR2(1000),
    DAPANA nvarchar2(500),
    DAPANB nvarchar2(500),
    DAPANC nvarchar2(500),
    DAPAND nvarchar2(500),
    DAPAN_DUNG nvarchar2(10000)
) 
/
create table KETQUA
(
    MSHS varchar(12),
    MAMONHOC varchar2(12),
    MADETHI varchar2(12),
    DIEMTHI float,
    THOIGIAN_HOANTHANH TIMESTAMP
)
/

---TẠO KHÓA CHÍNH
ALTER TABLE HOCSINH
ADD CONSTRAINT PK_HOCSINH PRIMARY KEY (MSHS)

ALTER TABLE GIAOVIEN
ADD CONSTRAINT PK_GIAOVIEN PRIMARY KEY (MSGV)

ALTER TABLE TAIKHOAN
ADD CONSTRAINT PK_TAIKHOAN PRIMARY KEY (ID)

ALTER TABLE MONHOC
ADD CONSTRAINT PK_MONHOC PRIMARY KEY (MAMONHOC)

ALTER TABLE DETHI
ADD CONSTRAINT PK_DETHI PRIMARY KEY (MADETHI)

ALTER TABLE DETHI_MONHOC
ADD CONSTRAINT PK_DETHI_MONHOC PRIMARY KEY (MADETHI,MAMONHOC)

ALTER TABLE CAUHOI
ADD CONSTRAINT PK_CAUHOI PRIMARY KEY (MACAUHOI,MAMONHOC)

ALTER TABLE KETQUA
ADD CONSTRAINT PK_KETQUA PRIMARY KEY (MSHS,MADETHI,MAMONHOC)

---TẠO KHÓA NGOẠI
ALTER TABLE HOCSINH
ADD CONSTRAINT FK_HOCSINH FOREIGN KEY (MSHS) REFERENCES TAIKHOAN(ID);

ALTER TABLE GIAOVIEN
ADD CONSTRAINT FK_GIAOVIEN FOREIGN KEY (MSGV) REFERENCES TAIKHOAN(ID);

ALTER TABLE GIAOVIEN
ADD CONSTRAINT FK_GIAOVIEN_MAMH FOREIGN KEY (MAMONHOC) REFERENCES MONHOC(MAMONHOC);

ALTER TABLE CAUHOI
ADD CONSTRAINT FK_CAUHOI FOREIGN KEY (MAMONHOC) REFERENCES MONHOC(MAMONHOC);

ALTER TABLE DETHI_MONHOC
ADD CONSTRAINT FK_DETHI_MONHOC_MMH FOREIGN KEY (MAMONHOC) REFERENCES MONHOC(MAMONHOC);
ALTER TABLE DETHI_MONHOC
ADD CONSTRAINT FK_DETHI_MONHOC_MDT FOREIGN KEY (MADETHI) REFERENCES DETHI(MADETHI);

ALTER TABLE KETQUA 
ADD CONSTRAINT FK_KETQUA_HOCSINH FOREIGN KEY (MSHS)  REFERENCES HOCSINH(MSHS);

ALTER TABLE KETQUA 
ADD  CONSTRAINT FK_KETQUA_MONHOC FOREIGN KEY (MAMONHOC) REFERENCES MONHOC(MAMONHOC);

ALTER TABLE KETQUA 
ADD  CONSTRAINT FK_KETQUA_MADETHI FOREIGN KEY (MADETHI) REFERENCES DETHI(MADETHI);

---------RÀNG BUỘC KHÓA-------------
ALTER TABLE DETHI
ADD CONSTRAINT UQ_DETHI_MADETHI UNIQUE (MADETHI);

--------------DROP KHÓA---------------
ALTER TABLE CAUHOI
DROP CONSTRAINT FK_DETHI_MONHOC;

ALTER TABLE CAUHOI DROP CONSTRAINT FK_CAUHOI;



-----------------------------NHẬP LIỆU
 
-- truoc khi nhap lieu phai cap quota tren tablespace (luu y chay tren user sys)
alter user CauHoiTracNghiem quota 100M on users;

alter session set NLS_DATE_FORMAT = 'DD-MM-YYYY';

-----------------------NHẬP LIỆU CHO BẢNG TÀI KHOẢN TRƯỚC-------------------------
SELECT * FROM TAIKHOAN

INSERT INTO TAIKHOAN (ID,MATKHAU) VALUES ('HS00001','123');
INSERT INTO TAIKHOAN (ID,MATKHAU) VALUES ('HS00002','123');
INSERT INTO TAIKHOAN (ID,MATKHAU) VALUES ('HS00003','123');
INSERT INTO TAIKHOAN (ID,MATKHAU) VALUES ('HS00004','123');
INSERT INTO TAIKHOAN (ID,MATKHAU) VALUES ('HS00005','123');

INSERT INTO TAIKHOAN (ID,MATKHAU) VALUES ('GV0001','123');
INSERT INTO TAIKHOAN (ID,MATKHAU) VALUES ('GV0002','123');
INSERT INTO TAIKHOAN (ID,MATKHAU) VALUES ('GV0003','123');
INSERT INTO TAIKHOAN (ID,MATKHAU) VALUES ('GV0004','123');
INSERT INTO TAIKHOAN (ID,MATKHAU) VALUES ('GV0005','123');

---------------------NHẬP LIỆU CHO BẢNG HỌC SINH TRƯỚC---------------------------
SELECT * FROM HOCSINH

drop user HS0007

delete from hocsinh where MSHS ='HS0007'

INSERT INTO HOCSINH (MSHS, HOTENHS, NGAYSINH, GIOITINH,DIACHI, LOP)
values ('HS00001',N'Nguyễn Thị Thùy Trang','01-02-2014',N'Nữ',NULL, NULL);
INSERT INTO HOCSINH (MSHS, HOTENHS, NGAYSINH, GIOITINH,DIACHI, LOP)
values ('HS00003',N'Nguyễn Thị Kim Ngọc', '01-02-2013',N'Nữ',NULL, NULL);
INSERT INTO HOCSINH (MSHS, HOTENHS, NGAYSINH, GIOITINH,DIACHI, LOP)
values ('HS00004',N'Nguyễn Xuân Phúc', '01-02-2014',N'Nam',NULL, NULL);
INSERT INTO HOCSINH (MSHS, HOTENHS, NGAYSINH, GIOITINH,DIACHI, LOP)
values ('HS00005',N'Trần Minh An', '01-02-2012',N'Nữ',NULL, NULL);

--GIÁO VIÊN
insert into GIAOVIEN (MSGV,hotengv,NGAYSINH, GIOITINH, MAMONHOC)
values ('GV0001', N'Trương Mỹ Kinh', '03-01-1984', N'Nữ', NULL);
insert into GiaoVien (MSGV,hotengv,NGAYSINH,GIOITINH,MAMONHOC)
values ('GV0002', N'Trần Hào', '30-4-1982', N'Nam', null);
insert into GiaoVien (MSGV,hotengv,NGAYSINH, GIOITINH, MAMONHOC)
values ('GV0003', N'Nguyễn Huỳnh Hoa', '30-4-1982', N'Nữ', null);
insert into GiaoVien (MSGV,hotengv,NGAYSINH, GIOITINH, MAMONHOC)
values ('GV0004', N'Lê Xuân Ngọc', '30-4-1982', N'Nữ', null);
insert into GiaoVien (MSGV,hotengv,NGAYSINH, GIOITINH, MAMONHOC)
values ('GV0005', N'Nguyễn Bình Minh', '30-4-1982', N'Nam', null);

select * from giaovien

---------------------NHẬP LIỆU CHO BẢNG MÔN HỌC TRƯỚC---------------------------
SELECT * FROM MONHOC

insert into MONHOC (MAMONHOC,TENMONHOC)
values ('MH00001', N'Tiếng Anh');
insert into MONHOC (MAMONHOC,TENMONHOC)
values ('MH00002', N'Địa Lý');
insert into MONHOC (MAMONHOC,TENMONHOC)
values ('MH00003', N'Gíao dục công dân');
insert into MONHOC (MAMONHOC,TENMONHOC)
values ('MH00004', N'Hóa học');
insert into MONHOC (MAMONHOC,TENMONHOC)
values ('MH00005', N'Toán');


---------------------NHẬP LIỆU CHO BẢNG ĐỀ THI TRƯỚC---------------------------
SELECT * FROM DETHI 
insert into DETHI (MADETHI,SOCAUHOI)
values ('DT00001',2);
insert into DETHI (MADETHI,SOCAUHOI)
values ('DT00002',2);
insert into DETHI (MADETHI,SOCAUHOI)
values ('DT00003',2);
insert into DETHI (MADETHI,SOCAUHOI)
values ('DT00004',2);



---------------------NHẬP LIỆU CHO BẢNG DETHI_MONHOC TRƯỚC---------------------------
SELECT * FROM DETHI_MONHOC

insert into DETHI_MONHOC (MADETHI,MAMONHOC,THOIGIAN_BATDAU)
values ('DT00001', 'MH00001',null);
insert into DETHI_MONHOC (MADETHI,MAMONHOC,THOIGIAN_BATDAU)
values ('DT00001', 'MH00002',null);
insert into DETHI_MONHOC (MADETHI,MAMONHOC,THOIGIAN_BATDAU)
values ('DT00001', 'MH00003',null);
insert into DETHI_MONHOC (MADETHI,MAMONHOC,THOIGIAN_BATDAU)
values ('DT00001', 'MH00004',null);
insert into DETHI_MONHOC (MADETHI,MAMONHOC,THOIGIAN_BATDAU)
values ('DT00001', 'MH00005',null);



alter table DETHI drop column THOIGIAN_BATDAU

alter table DETHI_MONHOC add THOIGIAN_BATDAU TIMESTAMP

alter session set NLS_DATE_FORMAT = 'DD-MM-YYYY';
ALTER SESSION SET NLS_TIMESTAMP_FORMAT = 'DD-MM-YYYY HH24:MI:SS';
UPDATE DETHI_MONHOC SET THOIGIAN_BATDAU='11-12-2024 13:33' where MADETHI = 'DT00001' and MAMONHOC = 'MH00001'
UPDATE DETHI_MONHOC SET THOIGIAN_BATDAU='11-12-2024 7:51' where MADETHI = 'DT00002' and MAMONHOC = 'MH00001'
UPDATE DETHI_MONHOC SET THOIGIAN_BATDAU='13-12-2024 13:00' where MADETHI = 'DT00001' and MAMONHOC = 'MH00002'
UPDATE DETHI_MONHOC SET THOIGIAN_BATDAU='13-12-2024 13:00' where MADETHI = 'DT00002' and MAMONHOC = 'MH00002'
UPDATE DETHI_MONHOC SET THOIGIAN_BATDAU='12-12-2024 18:00' where MADETHI = 'DT00001' and MAMONHOC = 'MH00003'
UPDATE DETHI_MONHOC SET THOIGIAN_BATDAU='12-12-2024 18:00' where MADETHI = 'DT00002' and MAMONHOC = 'MH00003'

UPDATE DETHI_MONHOC SET THOIGIAN_BATDAU= null

select TENMONHOC,MONHOC.MAMONHOC,MADETHI,THOIGIAN_BATDAU
from DETHI_MONHOC , MONHOC
where MONHOC.MAMONHOC = DETHI_MONHOC.MAMONHOC

---------------------NHẬP LIỆU CHO BẢNG CAU HOI TRƯỚC---------------------------
SELECT * FROM CAUHOI
DELETE FROM CAUHOI where macauhoi ='CH00003'



insert into CAUHOI (MAMONHOC,MACAUHOI,CAUHOI,DAPANA,DAPANB,DAPANC,DAPAND,DAPAN_DUNG)
values ('MH00001', 'CH00001', N'Economic analyses of soil_______ conservation investments may be done from private and social perspectives.', N'information', N'conservation', N'dictionary', N'supermarket', N'1');
insert into CAUHOI (MAMONHOC,MACAUHOI,CAUHOI,DAPANA,DAPANB,DAPANC,DAPAND,DAPAN_DUNG)
values ('MH00001', 'CH00002', N'The by-laws say that all dogs_______be kept on a lead in the park.', N'ought', N'need', N'must', N'have', N'3');

insert into CAUHOI (MAMONHOC,MACAUHOI,CAUHOI,DAPANA,DAPANB,DAPANC,DAPAND,DAPAN_DUNG)
values ('MH00002', 'CH00001', N'Nước ta nằm ở vị trí:', N'rìa phía Đông của bán đảo Đông Dương', N'rìa phía Tây của bán đảo Đông Dương', N'trung tâm châu Á', N'phía đông Đông Nam Á', N'0');
insert into CAUHOI (MAMONHOC,MACAUHOI,CAUHOI,DAPANA,DAPANB,DAPANC,DAPAND,DAPAN_DUNG)
values ('MH00002', 'CH00002', N'Nằm ở rìa phía Đông của bán đảo Đông Dương là nước:', N' Lào', N' Campuchia', N'Việt Nam', N'Mi-an-ma', N'2');

insert into CAUHOI (MAMONHOC,MACAUHOI,CAUHOI,DAPANA,DAPANB,DAPANC,DAPAND,DAPAN_DUNG)
values ('MH00003', 'CH00001', N'Pháp luật là quy tắc xử sự chung, được áp dụng đối với tất cả mọi người là thể hiện đặc trưng nào dưới đây của pháp luật?', N' Tính quy phạm phổ biến', N' Tính phổ cập', N'Tính rộng rãi', N'Tính nhân văn', N'0');
insert into CAUHOI (MAMONHOC,MACAUHOI,CAUHOI,DAPANA,DAPANB,DAPANC,DAPAND,DAPAN_DUNG)
values ('MH00003', 'CH00002', N'Pháp luật do Nhà nước ban hành và đảm bảo thực hiện ?', N' Bằng quyền lực Nhà nước', N' Bằng chủ trương của Nhà nước', N'Bằng chính sách của Nhà nước', N'Bằng uy tín của Nhà nước', N'0');

insert into CAUHOI (MAMONHOC,MACAUHOI,CAUHOI,DAPANA,DAPANB,DAPANC,DAPAND,DAPAN_DUNG)
values ('MH00004', 'CH00001', N'Số khối của nguyên tử X là 56, trong đó số neutron là 30. Số electron của nguyên tử X là?.', N'26', N'21', N'22', N'23', N'0');
insert into CAUHOI (MAMONHOC,MACAUHOI,CAUHOI,DAPANA,DAPANB,DAPANC,DAPAND,DAPAN_DUNG)
values ('MH00004', 'CH00002', N'Số electron tối đa trong phân lớp f là?', N'2', N'6', N'8', N'14', N'3');

insert into CAUHOI (MAMONHOC,MACAUHOI,CAUHOI,DAPANA,DAPANB,DAPANC,DAPAND,DAPAN_DUNG)
values ('MH00005', 'CH00001', N'Tính biệt thức ∆ từ đó tìm số nghiệm của phương trình: 9x2 − 15x + 3 = 0', N'∆ = 117 và phương trình có nghiệm kép', N'∆ = − 117 và phương trình vô nghiệm', N'∆ = 117 và phương trình có hai nghiệm phân biệt', N'∆ = − 117 và phương trình có hai nghiệm phân biệt', N'2');
insert into CAUHOI (MAMONHOC,MACAUHOI,CAUHOI,DAPANA,DAPANB,DAPANC,DAPAND,DAPAN_DUNG)
values ('MH00005', 'CH00002', N'Cho phương trình ax2 + bx + c = 0 (a ≠ 0) có biệt thức ∆ = b2 – 4ac > 0, khi đó, phương trình đã cho:', N'Vô nghiệm', N'Có nghiệm kép', N'Có hai nghiệm phân biệt', N'Có 1 nghiệm', N'2');


---------------------NHẬP LIỆU CHO BẢNG KETQUA TRƯỚC---------------------------
SELECT * from KETQUA
ALTER SESSION SET NLS_TIMESTAMP_FORMAT = 'DD-MM-YYYY HH24:MI:SS';
insert into KETQUA (MSHS,MAMONHOC,MADETHI,DIEMTHI,THOIGIAN_HOANTHANH)
values ('HS00001','MH00001','DT00002',10,'3-12-2024 22:38')

delete from KETQUA where mshs = 'HS00001'

        ---LỖI---






====================================================================================================================================================
---MÃ HÓA DATABASE BẰNG AES

--YÊU CẦU CẤP QUYỀN
GRANT EXECUTE ON DBMS_CRYPTO TO CauHoiTracNghiem;
GRANT CREATE PROCEDURE TO CauHoiTracNghiem;


CREATE OR REPLACE FUNCTION f_encryptData(p_data nvarchar2)
RETURN RAW IS
    encryptedData RAW(20000);
    l_key RAW(32) := UTL_RAW.CAST_TO_RAW('12345678901234567890123456789012'); 
    l_iv  RAW(16) := UTL_RAW.CAST_TO_RAW('1234567890123456');
BEGIN
    encryptedData := DBMS_CRYPTO.ENCRYPT(
        src => UTL_RAW.CAST_TO_RAW(p_data), 
        typ => DBMS_CRYPTO.ENCRYPT_AES256 + DBMS_CRYPTO.CHAIN_CBC + DBMS_CRYPTO.PAD_PKCS5, 
        key => l_key,
        iv  => l_iv);
    RETURN encryptedData;
END;

--- TEST HÀM MÃ HÓA & GIẢI MÃ
SELECT ID, MATKHAU AS MATKHAU FROM TAIKHOAN;

SELECT * FROM HOCSINH;

UPDATE TAIKHOAN SET MATKHAU =  'E1477168F2D5507DE165D10E2D6CBAFB'
where id = 'HS00001'

--thêm dữ liệu vào bảng bằng cách thêm hàm encrypt vào lệnh INSERT
INSERT INTO TAIKHOAN(ID, MATKHAU) VALUES('HS00003',f_encryptData('123'));

SELECT * FROM TAIKHOAN
SELECT ID, f_decryptData(MATKHAU) AS MATKHAU FROM TAIKHOAN;

delete
from HOCSINH
where MSHS = 'HS00007'

delete
from Taikhoan
where ID='HS00007'

drop user HS00007

UPDATE HOCSINH
    SET LOP = '13DHBM01', DIACHI = 'HCM'
WHERE MSHS = 'HS00001'

----ĐỀ THI NHIỀU MÔN HỌC & MÔN HỌC NHIỀU CÂU HỎI--------- 
SELECT 
    dt.MADETHI, 
    mh.MAMONHOC, 
    ch.MACAUHOI, 
    ch.CAUHOI, 
    ch.DAPANA, 
    ch.DAPANB, 
    ch.DAPANC, 
    ch.DAPAND, 
    ch.DAPAN_DUNG
FROM 
    DETHI dt
JOIN 
    DETHI_MONHOC dtmh ON dt.MADETHI = dtmh.MADETHI
JOIN 
    MONHOC mh ON dtmh.MAMONHOC = mh.MAMONHOC
JOIN 
    CAUHOI ch ON mh.MAMONHOC = ch.MAMONHOC
ORDER BY 
    dt.MADETHI, mh.TENMONHOC, ch.MACAUHOI;

select * from cauhoi


--------XÓA BẢNG------------
DROP TABLE GIAOVIEN
DROP TABLE KETQUA
DROP TABLE HOCSINH
DROP TABLE TAIKHOAN
DROP TABLE CAUHOI
DROP TABLE DETHI_MONHOC
DROP TABLE MONHOC
DROP TABLE DETHI

select cauhoi,dapana,dapanb,dapanc,dapand,f_decryptData(DAPAN_DUNG) 
from dethi, dethi_monhoc , cauhoi 
where dethi.madethi = dethi_monhoc.madethi  and dethi_monhoc.mamonhoc = cauhoi.mamonhoc


--------------------------------------------------------RSA--------------------------------------------------------------------------
SELECT dbms_java.get_ojvm_property('java_version') AS java_version FROM dual;

BEGIN
    DBMS_JAVA.LOADJAVA('-resolve -v -thin -user CauHoiTracNghiem/123@orcl D:\OneDrive - sbsdolar\Desktop\crypto4ora\crypto4ora.jar');
END;
/
GRANT CREATE PROCEDURE TO CauHoiTracNghiem;
GRANT EXECUTE ANY PROCEDURE TO CauHoiTracNghiem;
GRANT EXECUTE ON CRYPTO TO CauHoiTracNghiem;
GRANT EXECUTE ON DBMS_LOB TO CauHoiTracNghiem;
GRANT JAVAUSERPRIV TO CauHoiTracNghiem;
GRANT CREATE ANY JAVA TO CauHoiTracNghiem;
GRANT CREATE TRIGGER TO CauHoiTracNghiem;

--+++++++++++++++++++++++++++++++++++++++++++++++++++++++
--START : PLEASE DO NOT MAKE ANY CHANGES TO THIS SECTION.
--+++++++++++++++++++++++++++++++++++++++++++++++++++++++
SET define on
SET echo on
SET linesize 2048
SET escape off
SET timing on
SET trimspool on
SET serveroutput on
--++++++++++++++++++++++++++++++++++++++++++++++++++++++++
--END : PLEASE DO NOT MAKE ANY CHANGES TO THIS SECTION.        
--++++++++++++++++++++++++++++++++++++++++++++++++++++++++

CREATE OR REPLACE PACKAGE CRYPTO AS 
FUNCTION RSA_ENCRYPT(PLAIN_TEXT VARCHAR2,PRIVATE_KEY VARCHAR2) RETURN VARCHAR2
AS
LANGUAGE JAVA NAME 'com/dishtavar/crypto4ora/RSAUtil.encrypt (java.lang.String,java.lang.String) return java.lang.String';


FUNCTION RSA_DECRYPT(ENCRYPTED_TEXT VARCHAR2,PUBLIC_KEY VARCHAR2) RETURN VARCHAR2
AS
LANGUAGE JAVA NAME 'com/dishtavar/crypto4ora/RSAUtil.decrypt (java.lang.String,java.lang.String) return java.lang.String';


FUNCTION RSA_SIGN(HASH_MESSAGE VARCHAR2,PUBLIC_KEY VARCHAR2) RETURN VARCHAR2
AS
LANGUAGE JAVA NAME 'com/dishtavar/crypto4ora/RSAUtil.sign (java.lang.String,java.lang.String) return java.lang.String';


FUNCTION RSA_VERIFY(PLAIN_HASH VARCHAR2,SIGNNED_HASH VARCHAR2,PRIVATE_KEY VARCHAR2) RETURN BOOLEAN
AS
LANGUAGE JAVA NAME 'com/dishtavar/crypto4ora/RSAUtil.verify (java.lang.String,java.lang.String,java.lang.String) return java.lang.Boolean';

FUNCTION RSA_GENERATE_KEYS(KEY_SIZE NUMBER) RETURN VARCHAR2
AS
LANGUAGE JAVA NAME 'com/dishtavar/crypto4ora/GenerateKey.generateRSAKeys (java.lang.Integer) return java.lang.String';

END CRYPTO;
/

------- sau khi thá»±c thi xong => phÃ¡t sinh khÃ³a
SELECT CRYPTO.RSA_GENERATE_KEYS(KEY_SIZE => 1024) FROM DUAL;

---function xử lí khóa public và khóa private
CREATE OR REPLACE FUNCTION extract_keys(p_full_key CLOB, p_key_type VARCHAR2)
RETURN CLOB
IS
    v_start_pos INTEGER;
    v_end_pos INTEGER;
    v_result_key CLOB;
BEGIN
    IF p_key_type = 'PUBLIC' THEN --cắt chuỗi public key
        v_start_pos := INSTR(p_full_key, '****publicKey start*****') + LENGTH('****publicKey start*****');
        v_end_pos := INSTR(p_full_key, '****publicKey end****');
    ELSIF p_key_type = 'PRIVATE' THEN --cắt chuỗi privatekey
        v_start_pos := INSTR(p_full_key, '****privateKey start****') + LENGTH('****privateKey start****');
v_end_pos := INSTR(p_full_key, '****privateKey end****');
    ELSE
        RAISE_APPLICATION_ERROR(-20001, 'Invalid key type. Use "PUBLIC" or "PRIVATE".');
    END IF;
    v_result_key := DBMS_LOB.SUBSTR(p_full_key, v_end_pos - v_start_pos, v_start_pos);
    RETURN TRIM(v_result_key);
END;
/


drop TRIGGER encrypt_MSSH
BEFORE INSERT OR UPDATE ON HOCSINH
FOR EACH ROW
DECLARE
    v_full_key CLOB := CRYPTO.RSA_GENERATE_KEYS(KEY_SIZE => 1024);    
    v_public_key CLOB := extract_keys(v_full_key,'PUBLIC');
BEGIN
    IF :NEW.MSHS IS NOT NULL THEN
        :NEW.MSHS := CRYPTO.RSA_ENCRYPT(v_public_key,:NEW.MSHS);
    END IF;
END;

alter table cauhoi modify(DAPAN_DUNG nvarchar2(2000))

update cauhoi set DAPAN_DUNG = CRYPTO.RSA_ENCRYPT(DAPAN_DUNG,'MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCeautJPn9t6V5NcncuX7DHZdG+j/Hlfl9au9wmkjk1Tv85zf8FgmSKmnl/7vX5/+Gp8rbBamWETDX1akykeyKrS4uuYwFa4IPglvzAGGeLwd6N61uIZTb79nDECTf95/9ot2DepqFbzZrk4aoVR8vLPC/jduQcT7EFmkV13ZnrVwIDAQAB')

select CRYPTO.RSA_DECRYPT(DAPAN_DUNG,'MIICdwIBADANBgkqhkiG9w0BAQEFAASCAmEwggJdAgEAAoGBAJ5q60k+f23pXk1ydy5fsMdl0b6P8eV+X1q73CaSOTVO/znN/wWCZIqaeX/u9fn/4anytsFqZYRMNfVqTKR7IqtLi65jAVrgg+CW/MAYZ4vB3o3rW4hlNvv2cMQJN/3n/2i3YN6moVvNmuThqhVHy8s8L+N25BxPsQWaRXXdmetXAgMBAAECgYBjhQGossV08/1VJAqxLFYu/c0FLQKmzHv00T2dUZD051q5IqsJ9/9Xf3HCqAkI8/H9RMgAu+lockQXl57sWZrOBDLCFsNP32Q3FJC6iSILv+QKq9g5xa0SZgy0i/s9jQeqcgjIaX/eM30/hct02qBWSxjvrrYDdKFkzMa6GXe3MQJBAPvvp5zhsRNSgB1oyc5AZNDfpahtWlTKKvQ4uBp9SaT0rXZVXW026pYIyT7ICzh/cseYPQU4TOAmx34P1g1vXLkCQQCg+RbJxWlnZElh+2KKBTJO6DIc66uWP8kS439HHnsHrxAuU9K9dw3dOIm80Xh4wo/izFlMxPYAc2H32YfcPiCPAkEA2eVbCHrC1j1ihQ0ejX5wM59a/aMmn3MDV5q+0FpQGZVteY03csAugHk05VHLMqA4O5zWGe+pvayMmeFEdvY8MQJBAJm/0Gg/ygEa5IxVkzTI6dg8J0FAR89mdSM5b2P6VQBt0UKuhWa5w+A8FDLoz+xnyQ6Sp+iPZ3fevQACIaXXITkCQBsFfjhKTH875WHKDD7oKFdkfo6kZV3E7OQ0c3jdsZDmBm1doPLPlHKjpd39YeNklGcK2LNDnaLerI7t2iQi52Q=')
     from cauhoi

select dapan_dung from cauhoi

select * from HocsINH

SELECT CRYPTO.RSA_ENCRYPT('This is my secret message','MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCeautJPn9t6V5NcncuX7DHZdG+j/Hlfl9au9wmkjk1Tv85zf8FgmSKmnl/7vX5/+Gp8rbBamWETDX1akykeyKrS4uuYwFa4IPglvzAGGeLwd6N61uIZTb79nDECTf95/9ot2DepqFbzZrk4aoVR8vLPC/jduQcT7EFmkV13ZnrVwIDAQAB')
    FROM DUAL;
    
SELECT CRYPTO.RSA_DECRYPT('ElPQFVNCJR6ksuqvRIZTsFEac+sMKcpm3h8Z6h25HR4sJiQG16PftoXc3doKCPUw4aSs6a67jA7ax1M3SWyphePDSJfjKHaxAkGweAJM6FIWF9p1btZDsxufAG1TGzeApEqSaspJKEiSQzMbw8qElzqgGuJJzod9sDFLr/jx5vg=','MIICdwIBADANBgkqhkiG9w0BAQEFAASCAmEwggJdAgEAAoGBAJ5q60k+f23pXk1ydy5fsMdl0b6P8eV+X1q73CaSOTVO/znN/wWCZIqaeX/u9fn/4anytsFqZYRMNfVqTKR7IqtLi65jAVrgg+CW/MAYZ4vB3o3rW4hlNvv2cMQJN/3n/2i3YN6moVvNmuThqhVHy8s8L+N25BxPsQWaRXXdmetXAgMBAAECgYBjhQGossV08/1VJAqxLFYu/c0FLQKmzHv00T2dUZD051q5IqsJ9/9Xf3HCqAkI8/H9RMgAu+lockQXl57sWZrOBDLCFsNP32Q3FJC6iSILv+QKq9g5xa0SZgy0i/s9jQeqcgjIaX/eM30/hct02qBWSxjvrrYDdKFkzMa6GXe3MQJBAPvvp5zhsRNSgB1oyc5AZNDfpahtWlTKKvQ4uBp9SaT0rXZVXW026pYIyT7ICzh/cseYPQU4TOAmx34P1g1vXLkCQQCg+RbJxWlnZElh+2KKBTJO6DIc66uWP8kS439HHnsHrxAuU9K9dw3dOIm80Xh4wo/izFlMxPYAc2H32YfcPiCPAkEA2eVbCHrC1j1ihQ0ejX5wM59a/aMmn3MDV5q+0FpQGZVteY03csAugHk05VHLMqA4O5zWGe+pvayMmeFEdvY8MQJBAJm/0Gg/ygEa5IxVkzTI6dg8J0FAR89mdSM5b2P6VQBt0UKuhWa5w+A8FDLoz+xnyQ6Sp+iPZ3fevQACIaXXITkCQBsFfjhKTH875WHKDD7oKFdkfo6kZV3E7OQ0c3jdsZDmBm1doPLPlHKjpd39YeNklGcK2LNDnaLerI7t2iQi52Q=')
    FROM DUAL;



====================================================================================================================================================
----------------------------MÃ HÓA LAI (HYBRID ENCRYPTION)------------------------------  
--key '12345678901234567890123456789012' 

create or replace FUNCTION f_decryptData(encryptedData RAW,key_ASE RAW)
RETURN NVARCHAR2 IS
    decryptedData NVARCHAR2(20000);
    l_key RAW(32) := UTL_RAW.CAST_TO_RAW(key_ASE);
    l_iv  RAW(16) := UTL_RAW.CAST_TO_RAW('1234567890123456');
BEGIN
    -- Giải mã dữ liệu đã mã hóa
    decryptedData := UTL_RAW.CAST_TO_NVARCHAR2(DBMS_CRYPTO.DECRYPT(
        src => encryptedData, 
        typ => DBMS_CRYPTO.ENCRYPT_AES256 + DBMS_CRYPTO.CHAIN_CBC + DBMS_CRYPTO.PAD_PKCS5, 
        key => l_key,
        iv  => l_iv));
    RETURN decryptedData;
END;

--giải mã key AES bằng RSA--------------------------------------------------------
CREATE OR REPLACE FUNCTION f_decryptAESKey(p_encrypted_aes_key CLOB, p_private_key CLOB)
RETURN RAW IS
    decrypted_aes_key RAW(32);
BEGIN
    decrypted_aes_key := UTL_RAW.CAST_TO_RAW(CRYPTO.RSA_DECRYPT(p_private_key, p_encrypted_aes_key));
    RETURN decrypted_aes_key;
END;

--giải mã data bằng RSA--
-- Hàm giải mã dữ liệu ---------------------------------------------------------
CREATE OR REPLACE FUNCTION f_decryptHybrid(p_encrypted_data RAW, key_ASE VARCHAR2, p_private_key VARCHAR2)
RETURN NVARCHAR2 IS
    decryptedData NVARCHAR2(20000);
    l_decrypted_aes_key RAW(32) := CRYPTO.RSA_DECRYPT(key_ASE, p_private_key);
BEGIN
    decryptedData := f_decryptData(p_encrypted_data,l_decrypted_aes_key);
    RETURN decryptedData;
END; 
/

SELECT CRYPTO.RSA_ENCRYPT('12345678901234567890123456789012','MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCeautJPn9t6V5NcncuX7DHZdG+j/Hlfl9au9wmkjk1Tv85zf8FgmSKmnl/7vX5/+Gp8rbBamWETDX1akykeyKrS4uuYwFa4IPglvzAGGeLwd6N61uIZTb79nDECTf95/9ot2DepqFbzZrk4aoVR8vLPC/jduQcT7EFmkV13ZnrVwIDAQAB')
    FROM DUAL;
    
SELECT f_decryptData(CRYPTO.RSA_DECRYPT('UMkoN4Vxs5jH0RA0sBKZxn9hCvQzSCHkRRBimkbEQHxYxf/IEsQ2pHyj5XN6gBy1Wmwy5EqWkax0CUcMCg73iglv6MZRuFx0r3PGO3LYjdUhl5EoOd1lk3/67dLVJfuKgplaKOh5qrNxuZRwwmjdo0fGZVcgq7DOI3dxmN+bUhI=','MIICdwIBADANBgkqhkiG9w0BAQEFAASCAmEwggJdAgEAAoGBAJ5q60k+f23pXk1ydy5fsMdl0b6P8eV+X1q73CaSOTVO/znN/wWCZIqaeX/u9fn/4anytsFqZYRMNfVqTKR7IqtLi65jAVrgg+CW/MAYZ4vB3o3rW4hlNvv2cMQJN/3n/2i3YN6moVvNmuThqhVHy8s8L+N25BxPsQWaRXXdmetXAgMBAAECgYBjhQGossV08/1VJAqxLFYu/c0FLQKmzHv00T2dUZD051q5IqsJ9/9Xf3HCqAkI8/H9RMgAu+lockQXl57sWZrOBDLCFsNP32Q3FJC6iSILv+QKq9g5xa0SZgy0i/s9jQeqcgjIaX/eM30/hct02qBWSxjvrrYDdKFkzMa6GXe3MQJBAPvvp5zhsRNSgB1oyc5AZNDfpahtWlTKKvQ4uBp9SaT0rXZVXW026pYIyT7ICzh/cseYPQU4TOAmx34P1g1vXLkCQQCg+RbJxWlnZElh+2KKBTJO6DIc66uWP8kS439HHnsHrxAuU9K9dw3dOIm80Xh4wo/izFlMxPYAc2H32YfcPiCPAkEA2eVbCHrC1j1ihQ0ejX5wM59a/aMmn3MDV5q+0FpQGZVteY03csAugHk05VHLMqA4O5zWGe+pvayMmeFEdvY8MQJBAJm/0Gg/ygEa5IxVkzTI6dg8J0FAR89mdSM5b2P6VQBt0UKuhWa5w+A8FDLoz+xnyQ6Sp+iPZ3fevQACIaXXITkCQBsFfjhKTH875WHKDD7oKFdkfo6kZV3E7OQ0c3jdsZDmBm1doPLPlHKjpd39YeNklGcK2LNDnaLerI7t2iQi52Q=')
    FROM DUAL;
  


---------------------test------------------------ 
select f_decryptData(MATKHAU,'12345678901234567890123456789012'), ID from TAIKHOAN

SELECT * FROM TAIKHOAN

drop trigger encrypt_mk

-- Truy vấn giải mã dữ liệu
SELECT ID, f_decryptHybrid(MATKHAU,'UMkoN4Vxs5jH0RA0sBKZxn9hCvQzSCHkRRBimkbEQHxYxf/IEsQ2pHyj5XN6gBy1Wmwy5EqWkax0CUcMCg73iglv6MZRuFx0r3PGO3LYjdUhl5EoOd1lk3/67dLVJfuKgplaKOh5qrNxuZRwwmjdo0fGZVcgq7DOI3dxmN+bUhI=','MIICdwIBADANBgkqhkiG9w0BAQEFAASCAmEwggJdAgEAAoGBAJ5q60k+f23pXk1ydy5fsMdl0b6P8eV+X1q73CaSOTVO/znN/wWCZIqaeX/u9fn/4anytsFqZYRMNfVqTKR7IqtLi65jAVrgg+CW/MAYZ4vB3o3rW4hlNvv2cMQJN/3n/2i3YN6moVvNmuThqhVHy8s8L+N25BxPsQWaRXXdmetXAgMBAAECgYBjhQGossV08/1VJAqxLFYu/c0FLQKmzHv00T2dUZD051q5IqsJ9/9Xf3HCqAkI8/H9RMgAu+lockQXl57sWZrOBDLCFsNP32Q3FJC6iSILv+QKq9g5xa0SZgy0i/s9jQeqcgjIaX/eM30/hct02qBWSxjvrrYDdKFkzMa6GXe3MQJBAPvvp5zhsRNSgB1oyc5AZNDfpahtWlTKKvQ4uBp9SaT0rXZVXW026pYIyT7ICzh/cseYPQU4TOAmx34P1g1vXLkCQQCg+RbJxWlnZElh+2KKBTJO6DIc66uWP8kS439HHnsHrxAuU9K9dw3dOIm80Xh4wo/izFlMxPYAc2H32YfcPiCPAkEA2eVbCHrC1j1ihQ0ejX5wM59a/aMmn3MDV5q+0FpQGZVteY03csAugHk05VHLMqA4O5zWGe+pvayMmeFEdvY8MQJBAJm/0Gg/ygEa5IxVkzTI6dg8J0FAR89mdSM5b2P6VQBt0UKuhWa5w+A8FDLoz+xnyQ6Sp+iPZ3fevQACIaXXITkCQBsFfjhKTH875WHKDD7oKFdkfo6kZV3E7OQ0c3jdsZDmBm1doPLPlHKjpd39YeNklGcK2LNDnaLerI7t2iQi52Q=') AS DECRYPTED_MK
FROM TAIKHOAN;
---------------------------------------------------------------


--------Cấp quyền cho bảng trắc nghiêm------------------------------------------------
-----chay tren sys
GRANT CREATE USER TO cauhoitracnghiem;
GRANT ALTER USER TO cauhoitracnghiem;
GRANT GRANT ANY PRIVILEGE TO cauhoitracnghiem;
GRANT SELECT ON SYS.DBA_USERS TO CauHoiTracNghiem;
GRANT SELECT ON SYS.DBA_PROFILES TO CauHoiTracNghiem;
GRANT CREATE PROFILE TO CauHoiTracNghiem;
GRANT CREATE ROLE TO CauHoiTracNghiem;
GRANT GRANT ANY PRIVILEGE TO CauHoiTracNghiem;




---------------từ đoạn này là chạy ở cauhoitracnghiem nhakkkkkkkkkk-------------
-----kiểm tra quyền user-------------------------------------------------------
select * from DBA_USERS

---procedure tạo user-----------------------------------------------------------
create or replace procedure pro_create_user(username in varchar2, pass in varchar2, profile in varchar2 )
is 
begin
    EXECUTE IMMEDIATE 'CREATE USER ' || username || ' IDENTIFIED BY "' || pass || '"';
    EXECUTE IMMEDIATE 'grant create session to "' || username || '"';
    EXECUTE IMMEDIATE 'ALTER USER ' || username || ' PROFILE "' || profile || '"';
end;

SELECT * FROM SESSION_PRIVS;
--------------------------------------------------------------------------
create or replace function fun_check_account(user in varchar2)
return int 
is
  t varchar2(50);
  kq int;
begin
  select account_status into t from dba_users where username=user;
  if t is null then
    kq:=0;
  else 
    kq:=1;
  end if;
  return kq;
exception when others then kq:=0;
  return kq;
end;
------------------------------------------------------------------------
create or replace procedure pro_alter_user(username in varchar2, pass in varchar2)
is
begin
  execute immediate 'ALTER USER' || username || 'IDENTIFIED BY"' || pass || '"';
  
end;
--------------------------------------------------------------------------
create or replace procedure Pro_CrUser(username in varchar2, pass in varchar2,profile in varchar2)
is
  ckUser int:=fun_check_account(username);
begin
  if ckUser=0 then
    pro_create_user(username, pass, profile);
  else
    pro_alter_user(username,pass);
  end if;
  commit work;
end;

----- Phần quyền-----------------------------------------
alter session set "_ORACLE_SCRIPT"=true; 

create profile HocSinh limit
  password_life_time 60
  password_grace_time 10
  password_reuse_time 1
  password_reuse_max 5
  failed_login_attempts 3;
-------------------------------------------------------------

create or replace function fun_account_status(user in varchar2)
return varchar2
is
  t varchar2(50);
begin
  select account_status into t from DBA_USERS where username=user;
  return t;
exception when others then t:=' ';
  return t;
end;

-------- phân quyền(chạy từng dòng) ---------

create role DataEntry_HOCSINH
grant select,insert,update on HOCSINH to DataEntry_HOCSINH
grant select,insert on KETQUA to DataEntry_HOCSINH
grant select on DETHI_MONHOC  to DataEntry_HOCSINH
grant select on MonHoc  to DataEntry_HOCSINH
grant select on cauhoi to DataEntry_HOCSINH
grant select on dethi to DataEntry_HOCSINH
grant select on dethi_monhoc to DataEntry_HOCSINH
GRANT EXECUTE ON CRYPTO TO DataEntry_HOCSINH
grant execute on f_decryptData to DataEntry_HOCSINH
grant execute on f_encryptData to DataEntry_HOCSINH
----------------------------------------------------------

create role DataEntry_GIAOVIEN
grant select,insert,update on GIAOVIEN to DataEntry_GIAOVIEN
grant select,insert,update,delete on CAUHOI to DataEntry_GIAOVIEN
grant select,insert,update on KETQUA to DataEntry_GIAOVIEN
grant select on MonHoc to DataEntry_GIAOVIEN
grant select,insert,update on HOCSINH to DataEntry_GIAOVIEN
grant select,insert,update on DETHI_MONHOC to DataEntry_GIAOVIEN
grant select,insert,update on Dethi to DataEntry_GIAOVIEN
GRANT EXECUTE ON CRYPTO TO DataEntry_GIAOVIEN
grant execute on f_decryptData to DataEntry_GIAOVIEN
grant execute on f_encryptData to DataEntry_GIAOVIEN

------- Thủ tục phân quyền cho HOCSINH -------------------------

create or replace procedure quyen_hs (username in varchar2)
is
begin
  execute immediate 'GRANT DATAENTRY_HOCSINH TO"' || username || '"';
end;
----------------------------------------------------------------

create or replace procedure quyen_gv (username in varchar2)
is
begin
  execute immediate 'GRANT DATAENTRY_GIAOVIEN TO"' || username || '"';
end;

----test tạo user
alter session set "_ORACLE_SCRIPT"=true;

BEGIN
    Pro_CrUser('HS14', '123','HOCSINH');
END;

begin
    quyen_hs('HS14');
end;

drop user HS14







