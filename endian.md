>[!INFO] Intel x86 architecture uses little-endian, while many RISC architectures and older systems like IBM mainframes utilize big-endian.
### Big endian
- The most significant byte (MSB) of a mult-ibyte data value is stored at the lowest memory address.

### Little endian
- the least significant byte (LSB) is stored at the lowest memory address

##### Data interpretation
- when data is read from memory, the byte order determines how it is interpreted.
- NUXI problem : where the same byte sequence can represent different values depending on the endianness of the system reading it.

##### Cross-platform compatibility
- in network communications, different systems may use different byte orders.
- the standard network byte order is big-endian.
- Function like `hton` host-to-network and `ntoh` network-to-host are used to convert data to the appropriate byte order before transmission and upon receipt, ensuring the systems can communicate effectively regardless of their internal byte order.

##### Performance considerations
- little endian systems can sometimes offer performance advantages in certain operations, such as addition, where the least significant bytes are more likely to remain unchanged, allowing for simpler and faster processing.
