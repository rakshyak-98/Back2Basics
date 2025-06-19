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
