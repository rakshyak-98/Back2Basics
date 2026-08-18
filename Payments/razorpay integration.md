[[Payments]]

# razorpay integration

> razorpay integration — user clicks "Pay" on the Frontend.

## Mental model

**Say it in one breath:** razorpay integration — user clicks "Pay" on the Frontend.

### **The High-Level Architecture Flow**
1. **User clicks "Pay"** on the Frontend.
2. **Frontend calls Backend** to create a new "Order".
3. **Backend calls Razorpay API** to generate a unique `order_id`, saves it to your database as "Pending", and sends it back to the Frontend.
4. **Frontend opens Razorpay Checkout** using that `order_id`.
5. **User completes payment** via the Razorpay UI.
6. **Razorpay sends success tokens** back to the Frontend.
7. **Frontend sends those tokens to Backend** for verification.
8. **Backend verifies the cryptographic signature** to ensure the payment is genuine, then updates the database to "Paid".
9. **(Safety Net) Razorpay Webhook fires** to your Backend in case the user closed their browser before Step 7.
### Workflow
1. **Customer Places an Order**
- Customer visits website/application
- Selects items to purchase
- Clicks pay button
- Creates a `transaction_id` or `checkout_id`

## Related

[[Payments]]
