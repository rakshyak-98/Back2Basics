[rfc](https://datatracker.ietf.org/doc/html/rfc7519)

## JSON Web Token (JWT)
- URL-safe means of representing claims to be transferred between two parties.
- the claims in a JWT are encoded as a JSON object that is used as the payload of a JSON Web Signature (JWS) structure or as the plain-text of  a JSON Web Encryption (JWE) structure.
- these enable the claims to be digitally signed or integrity protected with a Message Authentication Code (MAX) and/or encrypted.

### JWT claims
- JWT claims Set represents a JSON object whose members are the claims conveyed by the JWT.
- The Claim Names within a JWT Claims Set must be unique.
- JWT parsers must either reject JWTs with duplicate Claims Names or use a JSON parser that returns only the lexically last duplicate member name, as specified in [here](https://datatracker.ietf.org/doc/html/rfc7519#section-15.12).
- there are three classes of JWT Claim Names:
	- Registered Claim Names
	-  Public Claim Names	
	- Private Claim Names