## **Quick Summary Table**

| **Normal Form** | **Rules**                                               |
| --------------- | ------------------------------------------------------- |
| **1NF**         | Atomic values, unique columns, no repeating groups.     |
| **2NF**         | 1NF + no partial dependency on part of a composite key. |
| **3NF**         | 2NF + no transitive dependency on non-prime attributes. |
## **1NF (First Normal Form)**
- **Rule**:  
  - Each cell contains a single value (atomic).  
  - Each column has a unique name.  
  - The order of rows and columns does not matter.  
- **Example**:  
  **Before (Not 1NF)**:
  ```
  | ID | Name       | Phone Numbers      |
  |----|------------|--------------------|
  | 1  | Alice      | 12345, 67890       |
  | 2  | Bob        | 54321             |
  ```
  **After (1NF)**:  
  ```
  | ID | Name       | Phone Number       |
  |----|------------|--------------------|
  | 1  | Alice      | 12345             |
  | 1  | Alice      | 67890             |
  | 2  | Bob        | 54321             |
  ```

---
## **2NF (Second Normal Form)**
- **Rule**:  
  - Must be in **1NF**.  
  - No partial dependency: Non-prime attributes should depend on the entire primary key, not just part of it (for composite keys).  
- **Example**:  
  **Before (Not 2NF)**:  
  ```
  | OrderID | ProductID | ProductName  | CustomerName |
  |---------|-----------|--------------|--------------|
  | 1       | 101       | Laptop       | Alice        |
  | 2       | 102       | Mobile       | Bob          |
  ```
  **Issue**: `ProductName` depends only on `ProductID`, not the full key (`OrderID, ProductID`).  
  **After (2NF)**:  
  - Split into two tables:  
    **Orders**:  
    ```
    | OrderID | ProductID | CustomerName |
    |---------|-----------|--------------|
    | 1       | 101       | Alice        |
    | 2       | 102       | Bob          |
    ```
    **Products**:  
    ```
    | ProductID | ProductName |
    |-----------|-------------|
    | 101       | Laptop      |
    | 102       | Mobile      |
    ```

---

## **3NF (Third Normal Form)**
- **Rule**:  
  - Must be in **2NF**.  
  - No transitive dependency: Non-prime attributes should not depend on other non-prime attributes.  
- **Example**:  
  **Before (Not 3NF)**:  
  ```
  | EmployeeID | EmployeeName | Department | DeptHead  |
  |------------|--------------|------------|-----------|
  | 1          | Alice        | HR         | Bob       |
  | 2          | Charlie      | IT         | Dave      |
  ```
  **Issue**: `DeptHead` depends on `Department`, not directly on `EmployeeID`.  
  **After (3NF)**:  
  - Split into two tables:  
    **Employees**:  
    ```
    | EmployeeID | EmployeeName | Department |
    |------------|--------------|------------|
    | 1          | Alice        | HR         |
    | 2          | Charlie      | IT         |
    ```
    **Departments**:  
    ```
    | Department | DeptHead     |
    |------------|--------------|
    | HR         | Bob          |
    | IT         | Dave         |
    ```

---
