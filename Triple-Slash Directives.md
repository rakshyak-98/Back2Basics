are single-line comments containing a single XML tag.
- the contents of the comment are used as [[compiler directives]].

> [!NOTE] Triple-Slash Directives are only valid at the top of their containing file.
- also serve as a method to order the output when using `out` or `outFile`.
	- files are emitted to the output file location in the same order as the input after preprocessing pass

> [!INFO] an easy way to think of triple-slash-reference-types directive are as an `import` for declaration packages.