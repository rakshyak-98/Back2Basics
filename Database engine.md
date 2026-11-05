## What is Page?
In database a page is fixed size block of data that the database reads or writes as a unit. Think of a page as a small container holding several rows, often around 16 kilobytes (page is a fixed size block on disk).

How a database read and writes data on disk?
The engine locates the page that contains employee 5, loads that page into memeory, and reads the salary from that record. Even if you ask for one column, the engine still works in terms of pages. If you update the salary, it changes the record in memeory, then later writes the whole page back to disk.

How two database talk to each other?