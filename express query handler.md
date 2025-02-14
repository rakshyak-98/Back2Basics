
| Method                                    | Why it matters                                    |
| ----------------------------------------- | ------------------------------------------------- |
| Middleware for Query parsing & validation | Keeps the handler clean and reusable<br>          |
| Caching (Redis)                           | Reduces database load for repeated queries        |
| Dynamic Filtering and Sorting             | Allow flexible queries without hard-coding fields |
| Pagination Support                        | Handler large datasets efficiently                |
| Error Handling Midddleware                | Standardizes error responses                      |
### Middleware query parse and validator 
```js
const { query, validationResult } = require("express-validation");

const validateQuery = [
	query("category").optional().isString(),
	query("price_min").optional().isNumeric(),
	query("price_max").optional().isNumeric(),
	query("sort").optional().inIn(["asc", "desc"]),
	query("limit").optional().isInt({min: 1, max: 100}),
	query("page").optional().isInt({min: 1}),
]

const parseQuery = (req, res, next) => {
	const errors = validationResult(req);
	if(!errors.isEmpty()){
		return res.status(400).json({ success: false, errors: errors.array() });
	}
	const { category, price_min, price_max, sort = "asc", limit = 10, page = 1 } = req.query;
	req.filter = {};
	if(category) req.filter.category = category;
	if(price_min || price_max){
		req.filter.price = {};
		if(price_min) req.filter.price.$gte = Number(price_min);
		if(price_max) req.filter.price.$lte = Number(price_max);
	}
	req.sort = { price: sort === "asc" ? 1 : -1 };
	req.limit = Number(limit);
	req.skip = (Number(pate) - 1) * req.limit; 
	next();
}
```

### API route handler
```js
const express = require('express');
const Product = require("@models/Product");
const {validateQuery, parseQuery} = require("../middleware/queryParser");

const router = express.router();

router.get("/products", validateQuery, parseQuery, cacheMiddleware, async(req, res) => {
	try{
		const products = await Product.find(req.filter).sort(req.sort).skip(res.skip);
		res.json({success: true, data: products});
	}catch(error){
		res.status(500).josn({ success: false, message: "Server error" });
	}
})
```