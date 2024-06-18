- prevent the queue or buffer from overflowing. This mechanism is often called *backpressure* in network applications.
>[!NOTE] Backpressure should exist in any system that connects producers to consumers. A rule of thumb is to look for unbounded queues in software systems, as they are a sign of the lack of backprssure.
One problem with asynchronous communication is the what happens when the producer is producing faster than the consumer is consuming? 
### BackPressure in TCP: Flow control
- The consumer's TCP stack stores incoming data in a receive buffer for the application to consume.
- The amount of data the producer's TCP stack can send is bounded by a *window* known to the producer's TCP stack, and it will pause sending data when the window is full.
- The consumer's TCP stack manages the window; when the app drains from the receive buffer, it moves the window forward and notifies the producer's TCP stack to resume sending.

### Why wait for writes to complete?
Because while the application is waiting, it cannot produce! The `socket.write()` will always succeed even if the runtime cannot submit more data to the OS due to full send buffer.
- data has to go somewhere, it goes to an unbounded internal queue in the runtime.
- which can cause unbounded memory usage.
`socket.pause()` is essential, because it is used to implement backpressure.