[Coroutines](https://en.wikipedia.org/wiki/Coroutine) are allow execution to be 
1. suspended
2. resumed
3. well suited for implementing familiar program components such as cooperative tasks, exceptions, event loops, iterators, infinite lists and pipes.
> [!NOTE] function whose execution you can pause

Two characteristics of co-routing:
1. values of data local to a co-routine persist between successive calls.
2. execution of a co-routine is suspended as control leaves it, only to carry on where it left off when control re-enters the co-routine at some later stage.
- co-routine are cooperatively multi-tasked, whereas threads are typically preemptively multi-tasked.
- co-routine provide concurrency 
- allow tasks to be performed out of order or in a changeable order, without changing the overall outcome. 
- do not provide parallelism, because the do not execute multiple tasks simultaneously.
The advantages of co-routines over threads are:
- used in a hard-realtime context (switching between co-routine need not involve any system calls or any blocking calls whatsoever), there is no need of synchronization primitives such as [[mutexes]], [[semaphores]] etc.
- in order to guard [[critical sections]] and there is no need for support from the operating system.
> Generators also known as semi-co-routines are a subset of co-routines.
