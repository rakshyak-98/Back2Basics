- process by which client-side JavaScript framework takes over a server-rendered HTML page and make it interactive by attaching event listeners to the HTML element.
- Hydration makes the static HTML interactive by enabling React's features like state management, event handling, and component lifecycle methods.
- ensuring the HTML is constant in SSR and CSR is crucial.
### Whey is Hydration important?
- SEO : Server-Side-Rendering (SSR) allow search engines to crawl fully rendered HTML, improving SEO. It also helps users see content faster since the HTML is generated on the server.
### How does Hydration work?
1. Server-Side-Rendering : Server renders the HTML content of a React component and sends it to the client. This HTML includes minimal JavaScript needed to bootstrap React.
2. Sending HTML to Client: Server sends the complete HTML to the browser. The user sees a fully rendered page quickly.
3. Hydration on the client: Once the HTML is loaded React's JavaScript bundle is downloaded and executed. React reads the already rendered HTML, builds the internal component tree, and attaches events listeners.