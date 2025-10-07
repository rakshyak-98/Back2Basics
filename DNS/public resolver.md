### **1. Public resolver’s job**

Public resolvers (like `8.8.8.8` or `1.1.1.1`) **don’t store domain → IP mappings permanently**.  
They act as **recursive resolvers**, meaning:

- They fetch the correct IP from the authoritative source on your behalf.
    
- They **cache** the answer temporarily (based on TTL).
    

---

### **2. Step-by-step resolution flow**

When you query `dig @8.8.8.8 example.com`, Google DNS performs this chain:

1. **Check local cache**
    
    - If already cached and TTL not expired → return instantly.
        
2. **If not cached → recursive lookup begins:**  
    a. Ask **root DNS servers** → “who handles `.com` TLD?”  
    b. `.com` TLD servers respond with NS (nameserver) for `example.com` (e.g. `ns1.examplehost.com`).  
    c. Public resolver then asks that **authoritative nameserver** for `example.com` → “what is its A record?”  
    d. Authoritative server replies: `example.com → 93.184.216.34`.
    
3. **Public resolver caches this** for the TTL (say, 3600s).
    
4. **Public resolver sends result back** to your machine.
    

---

### **3. Next requests**

When anyone else asks the same resolver for `example.com` within that TTL window,  
it returns the **cached IP**, avoiding the full lookup chain.

---

### **4. Summary logic**

```
User query → Public Resolver
   ↓
Cache hit? yes → return
        no → ask Root → TLD → Authoritative
   ↓
Store in cache (TTL)
   ↓
Return IP
```

---

### **5. Key separation**

- **Authoritative servers** = “source of truth” (where domain owner defines A/CNAME/MX records).
- **Public resolvers** = “smart cache middlemen” that find and remember answers.
---


## Trace the full DNS resolution path from your cli

**Run a full trace**
```bash
dig +trace <domain>;
```

## Classic DNS propagation/resolver difference issue

`nslookup <domain> <public dns server>` -> NXDOMAIN
google public DNS (`8.8.8.8`) does not yet have the record cached or the record hasn't propagated to it.

`nslookup <domain> 1.1.1.1` -> resolves correctly
	- Cloudflare DNS `1.1.1.1` has already received the update record.

> [!INFO]
> - DNS changes propagate asynchronously
> - Each resolver caches records based on TTL.
> - Some resolvers query authoritative servers sooner than other.
> - NXDOMAIN on 8.8.8.8 means either
> 	- Had cached an old non-existent state (before the A record was added), or
> 	- Hasn't queried the authoritative nameservers yet.