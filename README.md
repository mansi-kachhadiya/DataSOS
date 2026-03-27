# DataSOS
  
CREATE TABLE demo_view (id INT AUTO_INCREMENT PRIMARY KEY,
NAME VARCHAR(20),
email VARCHAR(110),
INDEX value_show (email,NAME));



CREATE TABLE demo_view3(
id INT AUTO_INCREMENT PRIMARY KEY,		
NAME VARCHAR(55),
data_flow JSON,
email VARCHAR(150),
date_time DATE,
date_time_combine DATETIME,
CONSTRAINT uniquw_value UNIQUE(NAME,email),
INDEX set_values (email)
)ENGINE=INNODB CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

INSERT INTO demo_view3(NAME, data_flow, email, date_time, date_time_combine)
  VALUES ("demoname",'{"name":"demo_name","age":26,"work":"all good"}',"abcd@hijk.lmn",'2026-02-27','2026-02-27 01:23:00');
  
#====add column
ALTER TABLE demo_view3 ADD user_rating INT;
ALTER TABLE demo_view3 ADD id_new INT;
ALTER TABLE demo_view3 ADD (test_column VARCHAR(5),test_column2 VARCHAR(5));

#=====modify column(chagne data type of existing column )
ALTER TABLE demo_view3 MODIFY user_rating VARCHAR(10);

#===== change column (chagne column name and data type)(old name ,new name , data type)
ALTER TABLE demo_view3 CHANGE user_rating rating VARCHAR(5)

#===== drop column 
ALTER TABLE demo_view3 DROP rating;

#=====rename table name 
ALTER TABLE demo_view3 RENAME TO demo_view_three;
ALTER TABLE demo_view_three RENAME TO demo_view3;

#=====app pkey
ALTER TABLE demo_view3 ADD PRIMARY KEY (id_new);

#===== drop primary key
ALTER TABLE demo_veiw3 DROP PRIMARY KEY (id_new);

#=====unique constraint add
ALTER TABLE demo_view3 ADD CONSTRAINT unique_name UNIQUE(email)

#==== drop unique constraint (unique constraint drop with help of index )(index and constraint name )
ALTER TABLE demo_view3 DROP INDEX unique_name;

