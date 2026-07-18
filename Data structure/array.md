- Why zero-based indexing -> primarily due to memory efficiency and pointer arithmetic in lower level implementation like C, which influenced most modern languages.

Offset from Base Address -> Arrays are stored in contiguous memory blocks. The first element is the array's base address (offset 0). To access the i-th element, the compiler simply computes `base + i * element_size` no subtraction needed.

> [!NOTE]
> A 1-based index require `base + (i - 1) * element_size`, adding an unnecessary operation that slows things down, especially in loops or large-scale access.