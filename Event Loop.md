An event loop as a runtime construct instead of as a library.
 - in other system their is a blocking call to start the event-loop.
 - in NodeJs their is no such start-the-event-loop call.
 - NodeJs simply enters the event loop after executing the input script.
 - NodeJs exits the event loop when there are no more callbacks to perform.
 