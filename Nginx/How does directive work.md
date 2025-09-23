## try_files
**PHP Applications**
```nginx
location / { 
	try_files $uri $uri/ /index.php?$query_string;
}
```

**Multiple Fallback options**
```nginx
location / { 
	try_files $uri $uri/ @backend;
} 

location @backend  { 
	proxy_pass http://localhost:3000;
}
```