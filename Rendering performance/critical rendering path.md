- is a crucial sequence of steps that web browsers follow to convert HTML, CSS and JavaScript into a visual representation on the screen.
### Pipeline
1. Document Object Model Construction
	1. the browser receives the HTML document and begins parsing it to create the DOM, a tree structure that represents the document's content and structure.
	2. this process involves converting bytes to characters, identifying tokens, and building nodes incrementally as HTML is received.
2. CSS Object Model (CSSOM) Construction
	1. after constructing the DOM, the browser processes CSS files to create the CSSOM.
	2. this model represents the styles associated with the element with the element in the DOM, allowing the browser to understand how to style the content.
3. Render Tree Creation
	1. browser combines the DOM and CSSDOM to create the Render Tree. This tree includes only the nodes that need to be rendered on the screen, omitting any elements that are not visible (like those with `display: none`) and applying styles from the CSSOM.
4. Layout Calculation
	1. browser calculates the layout, determining the size and position of each element on the page.
	2. this step involves calculating dimensions and positions based on the Render Tree, ensuring that all elements fit correctly withing the viewport.
5. Painting
	1. finally browser paints the pixels on the screen. This involves converting the layout into actual pixels, which may include rasterizing vector shapes and layering elements. The painting process can be optimized by minimizing the number of repainting operations when changes occur on the page.
6. Compositing
	1. if there are overlapping elements, the browser composites these layers together before displaying them on the screen.
	2. this step ensures that the final visual output is rendered correctly, taking into account the stacking order of layers.