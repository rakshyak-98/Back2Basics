### Workflow
1. **Customer Places an Order**
- Customer visits website/app
- Selects items to purchase
- Clicks pay button
- Creates a `transaction_id` or `checkout_id`

2. **Create Order from Server**
- Use Razorpay Orders API to create an order
- Razorpay processes details and returns an `order_id`

3. **Pass Order ID to Checkout**
- `order_id` is passed to client-side integration
- Razorpay Checkout UI displays payment methods

4. **Collect Payment Details**
- Customer selects payment option
- Payment details secured and stored by Razorpay as tokens

5. **Bank Authentication**
- Razorpay sends authentication request to customer's bank
- Bank authorizes amount deduction

> [!INFO] The `transaction_id` or `checkout_id` is created from **your backend API**, not directly by Razorpay. When creating an order, you'll generate this identifier in your server-side code before interacting with Razorpay
- ref: [stackoverflow razorpay how to get the order id](https://stackoverflow.com/questions/67243677/django-razorpay-how-to-get-the-order-id-after-payment-is-complete)