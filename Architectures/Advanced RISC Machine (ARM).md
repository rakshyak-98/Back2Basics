RISC (Reduced Instruction Set Computing)
- the PC is one of the [[32 general-purpose registers]]
- the PC often points to the address **two instructions ahead** due to the pipeline architecture. This means when you read the PC in ARM, it may reflect the address of the instruction currently being executed plus as offset (commonly `+8` bytes in ARM state)