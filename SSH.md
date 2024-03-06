# Understanding the SSH encryption and  Connection process
[post link](https://www.digitalocean.com/community/tutorials/understanding-the-ssh-encryption-and-connection-process)
- ssh key pairs begins after the symmetric encryption has been established.
- client-server model to authenticate two parties and encrypt the data.
- the client is responsible for beginning the initial [[TCP]] handshake with the server.
- ssh connection is established in two separate stages
	- first is to agree upon and establish encryption to protect future communication.
	- second to authenticate the user and discover whether access to the server should be granted.
- sever provides its public host key, which the client can use to check whether this was the intended host.
	- both party negotiate a session key using a version of something called [Diffie-Hellman algorithm]() combine their own private data with public data from the other system to arrive at an identical secret session key.
	- session key will be used to encrypt the entire session.
	- public and private key pairs used for this part of the procedure are completely separate from the SSH keys used to authenticate a client to the server.
## Understand Symmetric Encryption, Asymmetric Encryption and Hashes
- relationship of the encrypt and decrypt data determines whether an encryption scheme is [[symmetrical encryption]] or [[Asymmetrical Encryption]]
- Asymmetric key pairs that can be created are only used for authentication, not encrypting the connection.
- the first option from the client's list that is available on the server is used as the cipher algorithm in both directions.
- SSH uses asymmetric encryption, during initial key exchange process used to set up the symmetrical encryption. (produce temporary key paris and exchange the public key in order to produce the share secret that will be used for symmetrical encryption).
### SSH key pairs
- SSH key pairs can be used to authenticate a client to a server.
- client creates a key pairs and then uploads the public key to any remote server it wishes to access.
after the symmetrical encryption is established to secure communication between the server and client, the client must authenticate to be allowed access.
- the server can use the public key in the file to encrypt a challenge message to the client.
- if client can prove that it was able to decrypt this message, it has demonstrated that it owns the associated private key.
- then server can set up the environment for the client.
## Hashing
- ssh takes advantage of [[Cryptographic hashing]] for data manipulation
- each message sent after the encryption is negotiated must contain a MAC (Message Authentication Code) so that the other party can verify the packet integrity.
- the MAC is calculated from the symmetrical shared secret, the packet sequence number of the message, and the actual message content.
- the MAC itself is sent outside of the symmetrically encrypted area as the final part of the packet.
- recommend encrypting the data first and then calculating the MAC.