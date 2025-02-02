## Payment Capture in Razorpay

**Definition**:  
Payment capture in Razorpay is the process of confirming and securing a payment after it has been authorized. It ensures that the authorized amount is deducted from the customer's account and transferred to the merchant's account.

---

### Key Points:

1. **Authorization & Capture Flow**:
    
    - **Authorization**: The payment amount is blocked on the customer's card or bank account.
    - **Capture**: The merchant confirms the payment, ensuring the amount is actually debited.
2. **Automatic vs Manual Capture**:
    
    - **Automatic**: Payments are captured automatically upon successful authorization.
    - **Manual**: Merchants can capture payments later through the Razorpay dashboard or API.
3. **Time Limit**:
    
    - Payments must be captured within 5 days of authorization.
    - If not captured, the payment is automatically reversed to the customer.
4. **APIs for Manual Capture**:
    
    - Razorpay provides an API to capture payments (`POST /payments/:payment_id/capture`).  
        Example:
        
        ```json
        {
          "amount": 1000
        }
        ```
        
5. **Use Cases**:
    
    - **E-commerce**: Ensuring product availability before capturing payments.
    - **Subscription Services**: Verifying customer details before finalizing the charge.

---

### Advantages:

- **Prevents Fraud**: Ensures funds are authorized before transfer.
- **Better Control**: Manual capture allows businesses to confirm orders first.
- **Reduced Risk**: Funds can be refunded if the capture isn't processed.

### Disadvantages:

- **Delay in Settlement**: Manual capture may cause delays in payment settlement.
- **Reversal Risk**: Authorization expires if not captured in time.
