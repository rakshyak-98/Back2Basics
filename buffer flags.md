Buffers have various flags set by kernel to track their state:
- `V4L2_BUF_FLAG_MAPPED`: Buffer is mapped into application address space
- `V4L2_BUF_FLAG_QUEUED`: Buffer is on the incoming queue waiting to be filled
- `V4L2_BUF_FLAG_DONE`: Buffer has been filled and is on the outgoing queue