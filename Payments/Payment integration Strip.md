[[Payments]]

# Payment integration Strip

> Payment integration Strip — const handleCheckout = async () => {

## Mental model

**Say it in one breath:** Payment integration Strip — const handleCheckout = async () => {

```ts
  const handleCheckout = async () => {
    Swal.fire({
      title: 'Redirecting to Payment',
      text: 'You will be redirected to the payment page. Do you want to proceed?',
      icon: 'info',
      showCancelButton: true,
      confirmButtonText: 'Yes, proceed',
      cancelButtonText: 'Cancel',
    }).then(async (result) => {
      if (result.isConfirmed) {
        setIsLoading(true)
        try {
          const token = localStorage.getItem('user')
          // console.log('token=====>', token) // Example of retrieving the token
          const { results, status } = await change(
            'applications/checkout-session',
            {
              method: 'POST',
              body: {}, // Pass an empty body if no other data is required
              // isToken: true, // Not relying on automatic token handling
            }
          )
          if (status !== 200) {
            const errorMsg = results?.message || `HTTP error! status: ${status}`

## Related

[[Payments]]
