// =========================================================
// اطلاعات پرداخت
// =========================================================

// Authority سفارش از URL دریافت می‌شود.
//
// مثال:
// /api/orders/payment/mock/abc-123/
const pathParts =
    window.location.pathname
        .split("/")
        .filter(Boolean);


const authority =
    pathParts[pathParts.length - 1];


// =========================================================
// عناصر صفحه
// =========================================================

const successButton =
    document.getElementById(
        "success-payment-button"
    );


const failedButton =
    document.getElementById(
        "failed-payment-button"
    );


const messageElement =
    document.getElementById(
        "payment-message"
    );


// =========================================================
// ارسال نتیجه پرداخت به Backend
// =========================================================

async function submitPaymentResult(result) {

    try {

        // غیرفعال کردن دکمه‌ها
        successButton.disabled = true;
        failedButton.disabled = true;


        messageElement.textContent =
            "Processing payment...";


        const response =
            await fetch(
                `/api/orders/payment/mock/${authority}/result/`,
                {
                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body: JSON.stringify({
                        result: result
                    })
                }
            );


        const data =
            await response.json();


        if (!response.ok) {

            throw new Error(
                data.detail ||
                "Payment failed."
            );

        }


        // پرداخت موفق
        if (data.success) {

            messageElement.textContent =
                "Payment successful.";


            // انتقال به صفحه موفقیت
            window.location.href =
                data.redirect_url;


            return;
        }


        // پرداخت ناموفق
        messageElement.textContent =
            "Payment canceled.";


        // برگشت به Checkout
        setTimeout(() => {

            window.location.href =
                data.redirect_url;

        }, 1000);


    } catch (error) {

        console.error(
            "Payment error:",
            error
        );


        messageElement.textContent =
            error.message;


        // فعال کردن مجدد دکمه‌ها
        successButton.disabled = false;

        failedButton.disabled = false;

    }

}


// =========================================================
// پرداخت موفق
// =========================================================

successButton.addEventListener(
    "click",
    () => {

        submitPaymentResult(
            "success"
        );

    }
);


// =========================================================
// لغو پرداخت
// =========================================================

failedButton.addEventListener(
    "click",
    () => {

        submitPaymentResult(
            "failed"
        );

    }
);
