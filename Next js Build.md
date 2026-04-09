
## Generate Static files

```js
/** @type {import('next').NextConfig} */
const nextConfig = {
	output: "export",
  poweredByHeader: false,
  images: {
    // domains: ["theoterra.com"],
    remotePatterns: [
      {
        hostname: "theoterra.com",
        pathname: "**"
      }
    ]
  }
};

module.exports = nextConfig;

```