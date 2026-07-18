converting data (such as objects, database records, or responses) into a format that can be easily transferred over a network, stored, or processed.

- in backend API handlers, serialization is used to transform application data into JSON, XML, or other formats before sending it to clients.

> [!INFO] Serialization does not handle request queries directly.
> - Serialization is focused on transforming data for output (response)
> - handling request queries falls under parsing, validation and business logic before serialization happens.