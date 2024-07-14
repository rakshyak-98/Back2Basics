- linked list element is recursively defined as an object with `value` and `next`.
- the list can split into multiple parts and later joined back.
- list can be enhanced
	- we can add property `prev`. `tail` referencing the last element.

> [!NOTE] Drawback, we can't easily access an element by its number. In array it is direct reference. In list we need to start from the first item and go `next N` times to get the Nth element.
