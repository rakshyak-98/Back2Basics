```txt
CREATE TABLE table_name (
	column1 datatype constraints,
	column2 datatype constraints,
	...
)
```

```mysql
CREATE TABLE users(
	id INT AUTO_INCREMENT PRIMARY KEY,
	name VARCHAR(100) NOT NULL,
	role VARCHAR(50) DEFAULT 'guest'
)
```

### Create JSON type column

```sql
create table table_name(
	content JSON
)
```

```sql
insert into table_name (content) values ('{"name": "test user"}');
update table_name set content = '{"name": "james"}' where id = 1;
```

## update field
```mysql
update <tablename> Set <columnname> = <value> <condition>;
update employee Set name = "ram" where emp_id = 1000;
```
### update nested object value
```sql
UPDATE table_name
SET content = JSON_SET(
	content,
	'$.content.images.image2.url', 'http://example.com/1.png',
	'$.content.images.image2.url', 'http://example.com/1.png'
)
WHERE id = 1;
```

### update array field value
```sql
UPDATE section
SET content = JSON_SET(
  content,
  '$.content.offers[0].title',
  'Updated Offer Title'
)
WHERE id = 1;

UPDATE section
SET content = JSON_SET(
  content,
  '$.content.offers[2].image.url',
  'https://example.com/new-image.jpg'
)
WHERE id = 1;

```

> [!INFO]
> replace the entire array
```sql
UPDATE section
SET content = JSON_SET(
  content,
  '$.content.offers',
  JSON_ARRAY(
    JSON_OBJECT(
      'title', 'New Offer Title',
      'image', JSON_OBJECT(
        'alt', 'New Alt',
        'url', 'https://example.com/new-offer.jpg',
        'width', 800,
        'height', 400
      ),
      'descriptionLines', JSON_ARRAY('Line 1', 'Line 2')
    )
  )
)
WHERE id = 1;
```

> [!WARNING]
> Loses indexes, constraints - recreate manually if needed.
```mysql
-- Copy structure + insert data
INSERT INTO target_db.table_name SELECT * FROM source_db.table_name;
```

## Add columns to an existing table
```mysql
ALTER TABLE users
ADD (
	age INT
	is_active BOOLEAN DEFAULT TRUE,
	last_login TIMESTAMP
)
```

```mysql
ALTER TABLE table_name RENAME COLUMN old_name TO new_name;
ALTER TABLE table_name CHANGE COLUMN old_name TO new_name data_type;

```
### re-arrange columns
```mysql
ALTER TABLE table_name MODIFY column_name data_type AFTER other_column;
ALTER TABLE table_name MODIFY column_name data_tyep FIRST;
```
## How to do a table migration between database

#### If different server
```bash
mysqldump -u user -p source_db table_name > table_dump.sql

```

```bash
mysql -u user -p target_db < table_dump.sql

```
#### If server is same

> [!NOTE]
> Both column should of same data type
> Foreign reference column should have unique constraint (or primary key).
```mysql
CREATE TABLE target_db.table_name AS SELECT * FROM source_db.table_name; 

-- copy structure only
CREATE TABLE target_db.table_name LIKE source_db.table_name;
 
### Update table after query with join
```mysql
UPDATE hkAppNotification AS hk
LEFT JOIN jobDepartment AS jd
  ON jd.jobDepartmentName = hk.department
SET hk.department = jd.id;
```
