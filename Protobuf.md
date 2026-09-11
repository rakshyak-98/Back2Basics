```idl
syntax = "proto3"
message Person {
	string user_name = 1;
	int64 favorit_number = 2;
	repeated string interests = 3;
}
```
the `.proto` file defines the schema
- each field a **numeric field ID**

Produces class from the code generation tool that takes a schema definition. You application code can call this generate code to encode or decode records that conform to the schema.

> Protocol Buffers saves even more space by packing the field type and tag number into a single byte.