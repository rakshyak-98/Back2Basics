 The main reason for having call stack is:
 - keep track active sub-routine should return control when it finished executing.
 Active sub-routine is one that has called, but is yet to complete execution.
 For example, if a subroutine `DrawSquare` callas a sub-routine `DrawLine` from four different places, `DrawLine` must know where to return when  its execution completes. To accomplish this, the address (specific memory location) following the instruction that jumps to `DrawLine`, the return address, is pushed onto the top of the call stack with each call.
 > Adding a block's of sub-routine's entry to the call stack is sometimes called *winding*, and removing entries *unwinding*.
 
 The actual details of the the stack in a programming language depend upon the compiler, operating system and the available *instruction set*.
## Structure 
 Call stack is compose of [[stack frame]] also called activation records or activation frames. 