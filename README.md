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

### =============prectice on window function and logical deletion ============== ###

CREATE TABLE name_combination (
id INT AUTO_INCREMENT PRIMARY KEY,
last_name VARCHAR(120),
first_name VARCHAR(120),
extra_key VARCHAR(150),
STATUS VARCHAR(100) DEFAULT "pending",
INDEX index_on_last_frist_name (last_name,first_name),
CONSTRAINT unique_name UNIQUE (last_name,first_name,extra_key)
)ENGINE=INNODB CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
#insert data in extra key based on some find words
INSERT INTO `name_combination` (`extra_key`) SELECT TRIM(SUBSTRING_INDEX(case_name,"In Re: ",-1)) FROM `case_type_entry_table` WHERE LOCATE("In Re: ",case_name)>0;
INSERT INTO `name_combination` (`extra_key`) SELECT TRIM(SUBSTRING_INDEX(case_name,"vs. ",-1)) FROM `case_type_entry_table` WHERE LOCATE("vs. ",case_name)>0;
INSERT INTO `name_combination` (`extra_key`) SELECT TRIM(SUBSTRING_INDEX(case_name,"vs ",-1)) FROM `case_type_entry_table` WHERE LOCATE("vs ",case_name)>0;

#updating extra charectors that not usefull in searching
SELECT * FROM `name_combination` WHERE extra_key LIKE "%, et al%";

UPDATE name_combination SET extra_key = REGEXP_REPLACE(extra_key," et al","") WHERE extra_key LIKE "% et al%";

UPDATE name_combination SET extra_key = REGEXP_REPLACE(extra_key,", Inc.","") WHERE extra_key LIKE "%, Inc.%";

UPDATE name_combination SET extra_key = REGEXP_REPLACE(extra_key,", INC","") WHERE extra_key LIKE "%, INC%";
UPDATE name_combination SET extra_key = REGEXP_REPLACE(extra_key,", Sr.","") WHERE extra_key LIKE "%, Sr.%";
UPDATE name_combination SET extra_key = REGEXP_REPLACE(extra_key," Jr","") WHERE extra_key LIKE "% Jr%";
ROLLBACK;
UPDATE name_combination SET extra_key = REGEXP_REPLACE(extra_key,", III","") WHERE extra_key LIKE "%, III%";
UPDATE name_combination SET extra_key = REGEXP_REPLACE(extra_key,",","") WHERE extra_key LIKE "%,%";
UPDATE name_combination SET extra_key = REGEXP_REPLACE(extra_key," Living Trust dated March 21 1991","") WHERE extra_key LIKE "% Living Trust dated March 21 1991%";
UPDATE name_combination SET extra_key = REGEXP_REPLACE(extra_key," Inc.","") WHERE extra_key LIKE "% Inc.%";
UPDATE name_combination SET extra_key = REGEXP_REPLACE(extra_key," Co.","") WHERE extra_key LIKE "% Co.%";

#deleting not working records menually
DELETE FROM `name_combination` WHERE extra_key IN ("TOYOTA MOTOR SALES U.S.A.","Konocti Unified School District","DOE 1","All Terrain Motors",
"BB Opco LLC","INTERNAL REVENUE SERVICE a bureau of the United States Department of the Treasury",
"Clear Lake Riviera Community Association dba Kelseyville Riviera Community Association","Sutter Lakeside Hospital",
"State of California by and through the Department of California Highway Patrol","County of Lake.","Allstate Insurance Company"
);

#duplicate remove section
SELECT COUNT(*), extra_key FROM name_combination GROUP BY extra_key HAVING COUNT(extra_key)>1;

#understandig of window function 
SELECT *, ROW_NUMBER() OVER (PARTITION BY extra_key ORDER BY id) AS rn;

#selectiong value from partition and filtering
SELECT * FROM (
SELECT *, ROW_NUMBER() OVER (PARTITION BY extra_key ORDER BY id) AS rn FROM name_combination) table_1 WHERE table_1.rn > 1;

#sub query deletion 
DELETE FROM name_combination WHERE id IN (
SELECT id FROM (
SELECT *, ROW_NUMBER() OVER (PARTITION BY extra_key ORDER BY id) AS rn FROM name_combination) table_1 WHERE table_1.rn > 1);


#join deletion
DELETE n FROM name_combination n JOIN(
SELECT id, ROW_NUMBER() OVER (PARTITION BY extra_key ORDER BY id) AS rn FROM name_combination
) x1 ON n.id = x1.id WHERE x1.rn >1;


#partition in frist_name and last name
SELECT TRIM(SUBSTRING_INDEX(extra_key," ",1)) AS left_part, 
       TRIM(SUBSTRING_INDEX(extra_key," ",-1)) AS right_part FROM name_combination;
