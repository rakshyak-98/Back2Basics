don't start with "Which data structure do I know?". What operation are there in the problem which require a data structure?

**For any problem find the operations:**
- Access by index? -> Array/Slice -> "I care about position"
- Search by value/key? -> Hash Map -> "I have a key and want something associated with it"
- insert/delete? -> Hash Set/Linked List
- Need min/max quickly? -> Heap/Priority Queue -> "I repeatedly need to smallest/largest item"
- Need ordering? -> Balanced BST/Sorted structure
- Need uniqueness? -> Set
- Need key value lookup?
- Need FIFO/LIFO behaviour? -> Stack/Queue 
	- "Stack the most recent thing matters first"
	- "Queue the oldest thing should be processed first"
- Need relationships/connections? -> Tree/Graph
	- "Tree my data has hierarchy"
	- "Graph Things are connected to other thing."
- Need prefix/range queries? -> Trie


Hash map 
- You don't want to scan every user, access by a key. That's the nature hash-map problem

Heap/Priority Queue
- Give me the next smallest/largest element

### Decision process
1. What data do I have?
2. What operations do I need?
3. Which operation is expensive?
4. What data structure makes that operation cheap?
5. What are the time + space costs?

## Turning the problem into sequence of operations

### First ask "What must happen?"
- What would I do manually?

### Turn the problem into a "State"?
- What information do I need to remember while solving the problem?
- What Do I do when I seen the next element?

### Use this 5-question framework
- What is my input?
- What is my output?
- What information must I maintain?
- What happens for each input element?
- When am I done?

> An **invariant** is something that remains true while your algorithm runs. Once you know the invariant, the algorithm often becomes obvious.