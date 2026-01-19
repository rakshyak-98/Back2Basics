JSON Web Token (JWT) is a open standard (RFC 7519) for securely transmitting information between parties as a JSON object.
- JWT is stateless
- A JWT consists of three parts, separated by dots (.): Header.Payload.Signature

## Token blacklisting

- When a user logs out, grab the JWT from the header and store it in Redis.
- Set the Redis entry to expire at the same time the JWT would naturally expire. This keeps the database clean.
- On every protected request, check if the token exists in the blacklist.

### JWT revoke token using redis

```js
const redis = require('redis');
const client = redis.createClient();

// 1. Blacklist Middleware
async function checkBlacklist(req, res, next) {
  const token = req.headers.authorization?.split(' ')[1];
  
  if (!token) return res.status(401).send();

  // Check if token exists in Redis
  const isBlacklisted = await client.get(`blacklist_${token}`);
  
  if (isBlacklisted) {
    return res.status(401).json({ message: 'Token revoked. Please login again.' });
  }
  
  next();
}

// 2. Logout Route
async function logout(req, res) {
  const token = req.headers.authorization.split(' ')[1];
  const decoded = jwt.decode(token);
  
  // Calculate remaining time until JWT expires (in seconds)
  const ttl = decoded.exp - Math.floor(Date.now() / 1000);

  if (ttl > 0) {
    // Store in Redis with expiration
    await client.setEx(`blacklist_${token}`, ttl, 'true');
  }

  res.json({ message: 'Logged out successfully' });
}
```