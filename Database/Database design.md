
```md
//// Docs: https://dbml.dbdiagram.io/docs
//// -- LEVEL 1
//// -- Schemas, Tables and References

// Creating tables
// You can define the tables with full schema names

Table ecommerce.merchants {
	id int
	country_code int
	merchant_name varchar
	"created at" varchar
	admin_id int [ref: > U.id, not null]
	Indexes {
		(id, country_code) [pk]
	}
}

// If schema name is omitted, it will default to "public" schema.

Table users as U {
	id int [pk, increment] // auto-increment
	full_name varchar
	created_at timestamp
	country_code int
}

Table countries {
	code int [pk]
	name varchar
	continent_name varchar
}

// Creating references
// You can also define relaionship separately
// > many-to-one; < one-to-many; - one-to-one; <> many-to-many
Ref: U.country_code > countries.code
Ref: ecommerce.merchants.country_code > countries.code

//----------------------------------------------//

//// -- LEVEL 2
//// -- Adding column settings

Table ecommerce.order_items {
	order_id int [ref: > ecommerce.orders.id] // inline relationship (many-to-one)
	product_id int
	quantity int [default: 1] // default value
	Indexes {
		(order_id, product_id) [pk]
	}
}

Ref: ecommerce.order_items.product_id > ecommerce.products.id

Table ecommerce.orders {
id int [pk] // primary key
user_id int [not null, unique]
status varchar
created_at varchar [note: 'When order created'] // add column note
}

//----------------------------------------------//

//// -- Level 3
//// -- Enum, Indexes

// Enum for 'products' table below

Enum ecommerce.products_status {
	out_of_stock
	in_stock
	running_low [note: 'less than 20'] // add column note
}

// Indexes: You can define a single or multi-column index
Table ecommerce.products {
	id int [pk]
	name varchar
	merchant_id int [not null]
	price int
	status ecommerce.products_status created_at datetime [default: `now()`]
	Indexes {
		(merchant_id, status) [name:'product_status']
		id [unique]
	}
}

Table ecommerce.product_tags {
	id int [pk]
	name varchar
}

Table ecommerce.merchant_periods {
	id int [pk]
	merchant_id int
	country_code int
	start_date datetime
	end_date datetime
}

Ref: ecommerce.products.merchant_id > ecommerce.merchants.id // many-to-one
Ref: ecommerce.product_tags.id <> ecommerce.products.id // many-to-many

//composite foreign key
Ref: ecommerce.merchant_periods.(merchant_id, country_code) > ecommerce.merchants.(id, country_code)
Ref user_orders: ecommerce.orders.user_id > public.users.id

```

### Independent scalar value

- the value is stored as its own column. It is treated like a normal value that can be set independently

| subtotal | tax | discount | total_amount |
| -------- | --- | -------- | ------------ |
| 100      | 10  | 5        | 105          |
- Here `total_amount` is an **independent scalar value** because it is stored directly, rather than always being computed.
- rather then a mathematically enforced derivative of its components the database simply stores whatever value is provided.
- Since the database is not enforcing the relationship, it may accept inconsistent data.

> An **Independent scalar value** is a single stored field whose value is **not automatically derived or constrained by other fields** allowing it to become inconsistent with related data.

> [!NOTE]
> Instead of storing `total_amount` independently compute it whenever needed, or use a generated/computed column so the database guarantees consistency. This prevents mathematically invalid rows from being stored.


#### Pattern A : Deterministic Check Constraints

```sql
-- Enforce invariant on orders table
ALTER TABLE orders ADD CONSTRAINT chk_orders_amount_payable
CHECK (
  amount_payable = (base_amount - COALESCE(discount_amount, 0.00))
);

-- Enforce invariant on invoices table
ALTER TABLE invoices ADD CONSTRAINT chk_invoices_total_amount
CHECK (
  total_amount = (
    subtotal 
    - COALESCE(discount_amount, 0.00) 
    + COALESCE(tax_amount, 0.00)
  )
);
```

#### Pattern B : Stored Generated columns

Instead of forcing the application to pass the computed `total_amount` over the network, remove it from the `INSERt/UPDATE` payload entirely. The database derives and stores the aggregate mathematically during the write operation.

```sql
-- Drop the application-provided columns
ALTER TABLE orders DROP COLUMN amount_payable;
ALTER TABLE invoices DROP COLUMN total_amount;

-- Replace with storage-layer generated columns
ALTER TABLE orders ADD COLUMN amount_payable DECIMAL(10,2) 
GENERATED ALWAYS AS (
  base_amount - COALESCE(discount_amount, 0.00)
) STORED;

ALTER TABLE invoices ADD COLUMN total_amount DECIMAL(10,2) 
GENERATED ALWAYS AS (
  subtotal - COALESCE(discount_amount, 0.00) + COALESCE(tax_amount, 0.00)
) STORED;
```

## No Transaction Boundary Grouping

It means the audit log records **what changed**, but **not which changes belonged to the same transaction**.
	- Group all audit entries that belong to the same business transaction.
	- Although for different tables changed, they all belong to the same business transaction.

```sql
BEGIN;

UPDATE orders
SET status = 'PAID'
WHERE id = 101;

INSERT INTO payment_transactions (...);

INSERT INTO entitlements (...);

COMMIT;
```
- Nothing indicates these 3 audit rows came from **the same transaction**

Question you cannot answer:
- Did these three changes happen together?
- Were they committed atomically?
- Was payment inserted before entitlement?
- Did another transaction modify data between them?
- Which audit rows belong to one user action?

### With `transaction_correlation_id`

When `transaction_correlation_id` is stored in an `audit_log` table, its purpose is **not to identify the audit record itself**, but to group all audit entries that belong to the same business transaction.

> [!NOTE]
> The `transaction_correlation_id` should be created once, at the beginning of the business operation, before the database transaction starts (or immediately after it begins), and then passed unchanged throughout the entire request.

```txt
HTTP Request
     │
Generate UUID
     │
Store in request context
     │
Pass to all repositories/services

Reason:

- Same ID can be used in:
    - database
    - application logs
    - HTTP logs
    - Kafka messages
    - microservices
    - audit logs
```


Audit table:

| log_id | transaction_correlation_id | table                |
| -----: | -------------------------- | -------------------- |
|      1 | TX-89AF                    | orders               |
|      2 | TX-89AF                    | payment_transactions |
|      3 | TX-89AF                    | entitlements         |
Now auditor can query:
```sql
SELECT *
FROM audit_log
WHERE transaction_correlation_id = 'TX-89AF';`
```

Result
```txt
orders UPDATE
payment_transactions INSERT
entitlements INSERT
```
This proves these changes were part of one **atomic database transaction**.

**Why it matters:**
- Auditing: Verify all expected changes occurred together.
- Compliance: Demonstrate atomicity during investigations.
- Debugging: Reconstruct a complete business operation.
- Forensics: Detect partial updates or unexpected changes.

> [!NOTE]
> Without a transaction correlation ID, auditors must infer relationships using timestamps, user IDs, or session IDs, Which are unreliable because multiple transactions can occur within the same time window or session.

## Overlapping validity periods

occur when two or more distinct timeframes (or date ranges) share a common segment of time.

This concept frequently arises in database management, scheduling, HR systems, and software engineering (often referred to as temporal data). Managing validity periods effectively is crucial because overlaps can cause system conflicts, such as billing a customer twice for the same subscription or assigning two employees to a mutually exclusive shift.

### Understanding the Overlap logic

The most common challenge with validity periods is writing the logic to detect if an overlap exists.

A common mistake is trying to check if the start or end date of one period falls strictly inside the other. This often misses edge cases where one period completely engulfs another. The most robust, foolproof way to check if two periods, Period A and Period B overlap is to use this simple formula:
Period A starts before (or when) Period B ends AND Period A and Period B ends after (or when) Period B starts.

## Multi-Tenancy Boundary Violations

In a multi-tenant SaaS application, every row of tenant-specific data must belong to exactly one tenant, unless the table is explicitly designed to hold globally shared reference data.