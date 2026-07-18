is a middleware for Express JS that parses user-agent strings from incoming HTTP requests.
- it helps identify details about the client making the request

```js
import express from 'express';
import useragent from 'express-useragent';

const app = express();
app.use(useragent.express()); // Middleware to parse user-agent

app.get('/', (req, res) => {
    res.json({
        browser: req.useragent.browser,
        version: req.useragent.version,
        os: req.useragent.os,
        platform: req.useragent.platform,
        isMobile: req.useragent.isMobile,
        isDesktop: req.useragent.isDesktop,
    });
});

app.listen(3000, () => console.log('Server running on port 3000'));

```