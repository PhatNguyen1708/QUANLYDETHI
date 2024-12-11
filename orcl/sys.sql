alter session set "_ORACLE_SCRIPT"=true; 

create user CauHoiTracNghiem identified by 123

grant create session to CauHoiTracNghiem

grant create table to CauHoiTracNghiem

alter user CauHoiTracNghiem quota 100M on users

GRANT SELECT ON SYS.DBA_USERS TO CauHoiTracNghiem;
GRANT SELECT ON SYS.DBA_PROFILES TO CauHoiTracNghiem;
GRANT CREATE PROFILE TO CauHoiTracNghiem;
GRANT CREATE ROLE TO CauHoiTracNghiem;

create user GV0001 identified by 123
grant create session to GV0001
alter user GV0001 PROFILE HocSinh
GRANT DATAENTRY_GiaoVien TO GV0001

----------ghi nhật ký và giải trình sử dụng Standard Auditing, trigger

CREATE TABLE audit_log(
    logID NUMBER PRIMARY KEY,
    actionTime TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    userRole VARCHAR2(50),  --HOC SINH HOAC GIAO VIEN
    ID VARCHAR2(12),
    actionType VARCHAR2(50), --INSERT, UPDATE, DELETE
    tableName VARCHAR2(50),
    details NVARCHAR2(2000)
)

CREATE OR REPLACE drop TRIGGER trg_questions_audit
AFTER INSERT OR UPDATE OR DELETE ON CAUHOI
FOR EACH ROW
BEGIN
    IF INSERTING THEN
        INSERT INTO audit_log (userRole, ID, actionType, tableName, details)
        VALUES ('GIAOVIEN', USER, 'INSERT', 'CAUHOI', N'Đã thêm câu hỏi: ' || :NEW.CAUHOI);
    ELSIF UPDATING THEN
        INSERT INTO audit_log (userRole, ID, actionType, tableName, details)
        VALUES ('GIAOVIEN', USER, 'UPDATE', 'CAUHOI',
                'Cập nhật câu hỏi từ: ' || :OLD.CAUHOI || ' thành: ' || :NEW.CAUHOI);
    ELSIF DELETING THEN
        INSERT INTO audit_log (userRole, ID, actionType, tableName, details)
        VALUES ('GIAOVIEN', USER, 'DELETE', 'CAUHOI', 'Đã xóa câu hỏi: ' || :OLD.CAUHOI);
    END IF;
END;
/
CREATE OR REPLACE drop TRIGGER trg_student_answers_audit
AFTER INSERT ON KETQUA
FOR EACH ROW
BEGIN
    INSERT INTO audit_log (userRole, ID, actionType, tableName, details)
    VALUES ('HOCSINH', :NEW.MSHS, 'INSERT', 'KETQUA',
            N'Đã nộp bài ' || :NEW.MAMONHOC || N', Mã đề thi: ' || :NEW.MADETHI || N', vào lúc: ' || :NEW.THOIGIAN_HOANTHANH);
END;


