Their reason to pause the `data` event. In callback-based code, when the event handler returns, the runtime can fire the next `data` event if it is not paused. 
- The problem is that the completion of the event callback doesn't mean the completion of the event handling the handling can continue with further callbacks. 
- And the interleaved handling can cause problems. 
- Considering that the data is an ordered sequence of bytes. This situation is called *race condition* and is a class of problems related to [[Concurrency]]. In this situation, unwanted concurrency is introduced.