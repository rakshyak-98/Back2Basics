IPFS is a decentralized, [[P2P (Peer-to-Peer)]] file system that aims to make the we faster, safer, and more open. It allows users to store and share files in a distributed network of computers rather than relying on a central server.
- enables content-addressed file storage, meaning each file is identified by its unique hash, ensuring data integrity and availability across the network.

### Key features
- **Decentralized**: No central server stores the data. Instead, files are distributed across a network of nodes.
- **Content Addressing**: Each file is assigned a unique identifier (CID), generated based on its contents. This ensures the file’s integrity (i.e., it cannot be altered without changing its CID).
- **P2P Network**: Files are stored across multiple nodes in the network, and users can retrieve files from the closest available node, improving speed and reliability.
- **Versioning**: IPFS allows you to track and version changes in files, similar to Git.
- **File Duplication**: Files are only stored once across the network, reducing redundancy.

## How IPFS Works
Content Addressing: a file is uploaded to IPFS, it is broken into smaller chunks (blocks). Each block is assigned a unique cryptographic hash (CID). These CIDs are used to identify and retrieve the file from the network

Storing Files: The file is distributes across multiple nodes in the IPFS network. A node can store the file locally or cache it temporarily. Other nodes retrieve the file using its CID.

Retrieving Files: To access a file, you provide the CID (hash of the file). The IPFS network searches for the file by its CID and retrieves it from the nearest available node.

Distributed Hash Table (DHT): IPFS uses a [[DHT]] to store mappings between CIDs and the nodes that store the data. This allows efficient file retrieval in the decentralized network.

Pinning: To ensure files remain accessible, they can be "pinned" on a node. This prevents the file from being garbage collected.