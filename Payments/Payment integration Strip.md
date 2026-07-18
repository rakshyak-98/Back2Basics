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
            Swal.fire('Error', errorMsg, 'error')
            return
          }

          // console.debug(results)

          if (results?.success?.data?.url) {
            Swal.fire({
              title: 'Redirecting...',
              html: `
                <p>You will be redirected to the payment page shortly.</p>
                <div style="display: flex; justify-content: center; align-items: center; height: 100px; margin-top: 10px;">
                  <div style="display: flex; gap: 10px;">
                    <div class="pulsing-dot" style="width: 15px; height: 15px; background-color: #007bff; border-radius: 50%; animation: pulse 1s infinite;"></div>
                    <div class="pulsing-dot" style="width: 15px; height: 15px; background-color: #007bff; border-radius: 50%; animation: pulse 1s infinite 0.2s;"></div>
                    <div class="pulsing-dot" style="width: 15px; height: 15px; background-color: #007bff; border-radius: 50%; animation: pulse 1s infinite 0.4s;"></div>
                  </div>
                </div>
                <style>
                  @keyframes pulse {
                    0%, 100% { transform: scale(1); opacity: 1; }
                    50% { transform: scale(1.5); opacity: 0.5; }
                  }
                </style>
              `,
              showConfirmButton: false,
              allowOutsideClick: false,
              didOpen: () => {
                setTimeout(() => {
                  window.location.href = results.success.data.url
                }, 1500)
              },
            })
          } else {
            Swal.fire('Error', 'No checkout URL received.', 'error')
          }
        } catch (error) {
          console.error('Checkout Error:', error)
          Swal.fire(
            'Error',
            'Something went wrong! Please try again later.',
            'error'
          )
        } finally {
          setIsLoading(false)
        }
      } else {
        Swal.fire('Cancelled', 'Payment process was cancelled.', 'info')
      }
    })
  }
```