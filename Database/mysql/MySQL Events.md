```mysql
CREATE EVENT cleanup_event
ON SCHEDULE EVERY 1 DAY
DO
	DELETE FROM sessions WEHRE expired = 1;
```