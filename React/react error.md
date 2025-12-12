
```text
X-Content-Type-Options: nosniff

```

`X-Content-Type-Options` -> "Hey browser trust the file type I told you (like `.js` or `.css`) Don't try to be smart and guess different type."

Some hackers uploaded a file that looks like an image but is actually malicious code. The browser might "sniff" it and think "oh this is actually JavaScript" and run the bad code.