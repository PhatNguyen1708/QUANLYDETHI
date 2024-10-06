alter session set "_ORACLE_SCRIPT"=true; 

create user CauHoiTracNghiem identified by 123

grant create session to CauHoiTracNghiem

grant create table to CauHoiTracNghiem

alter user CauHoiTracNghiem quota 100M on users

