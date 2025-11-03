### JSON Conversion
```mysql
SELECT JSON_OBJECT('id', id, 'name', name) FROM users;
```

```mysql
SELECT JSON_EXTRACT(json_column, '$.key') AS value
FROM table_name;

-- shorthand operator
SELECT data->'$.username' AS username
FROM Users;

SELECT
  data->>'$.id' AS id,
  data->>'$.name' AS name,
  data->>'$.age' AS age
FROM People;
```

```mysql
-- array aggregator with group by
SELECT
  user_id,
  JSON_ARRAYAGG(email) AS emails
FROM user_emails
GROUP BY user_id;
```

```mysql
SELECT
  user_id,
  JSON_ARRAYAGG(JSON_OBJECT('id', post_id, 'title', title)) AS posts
FROM user_posts
GROUP BY user_id;

```
