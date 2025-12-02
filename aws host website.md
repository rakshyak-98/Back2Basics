
```bash
aws s3 website s3://$BUCKET --index-document index.html --error-document error.html	
```
- turns a normal s3 bucket into a static website.

|Part|Meaning|
|---|---|
|`aws s3 website`|“Hey S3, I want website hosting mode”|
|`s3://$BUCKET`|The bucket you are configuring (e.g., s3://my-free-website-1736438210)|
|`--index-document index.html`|When someone visits the root URL[](http://bucket.s3-website...), **automatically show index.html**|
|`--error-document error.html`|If a page is not found (404), show error.html instead of the ugly default XML error|