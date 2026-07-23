**NAT traversal** is the process of enabling two devices behind NATs to communicate with each other.

---

## What is NAT?

A **Network Address Translation (NAT)** device (usually your home/office router) maps **private IP addresses** to a **public IP address**.

Example:

```text
Internet
     |
Public IP: 203.0.113.10
     |
+------------------+
|   NAT Router     |
+------------------+
     |
----------------------------
|                          |
192.168.1.10           192.168.1.20
Browser A              Browser B
```

The devices have **private IPs**, which are **not reachable directly** from the Internet.

---

## The problem

Suppose two users want to start a WebRTC call.

```text
User A
192.168.1.10
      |
     NAT A
      |
 Internet
      |
     NAT B
      |
192.168.2.15
User B
```

Neither knows how to directly reach the other's private IP.

Even if they exchange:

```text
A: 192.168.1.10
B: 192.168.2.15
```

these addresses are only valid inside their own local networks.

---

## NAT traversal

NAT traversal is the set of techniques used to overcome this problem.

Typical steps:

1. Discover the public IP and port (**STUN**).
    
2. Attempt a direct connection (**ICE**).
    
3. If direct communication fails, relay traffic through **TURN**.
    

---

## Example

Without NAT traversal:

```text
Browser A  X------X  Browser B
```

Connection fails.

With NAT traversal:

```text
Browser A
     |
   STUN
     |
Learns public IP

Then

Browser A <-------------> Browser B
        Direct connection
```

If that still fails:

```text
Browser A ---> TURN ---> Browser B
```

---

## Technologies involved

| Technology | Purpose                                             |
| ---------- | --------------------------------------------------- |
| **STUN**   | Discover public IP and port                         |
| **ICE**    | Try different connection paths                      |
| **TURN**   | Relay traffic when direct connection isn't possible |

---

## Real-world analogy

Imagine two people inside office buildings.

- **Private IP** = their desk extension number.
    
- **Public IP** = the company's main phone number.
    
- **NAT traversal** = figuring out how they can call each other despite each being behind a company phone system.
    
    - Ask the receptionist for the external number (**STUN**).
        
    - Try calling directly (**ICE**).
        
    - If direct calls aren't allowed, route the call through an operator (**TURN**).
        

---

## Summary

- **NAT traversal** = techniques for enabling communication through NAT devices.
    
- It is needed because devices behind NAT are not directly reachable from the Internet.
    
- Common protocols:
    
    - **STUN** → discover public address.
        
    - **ICE** → find the best connection path.
        
    - **TURN** → relay traffic if direct connectivity fails.