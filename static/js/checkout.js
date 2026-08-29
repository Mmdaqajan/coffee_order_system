// =========================================================
// عناصر صفحه Checkout
// =========================================================

const form =
    document.getElementById(
        "checkout-form"
    );


const itemsContainer =
    document.getElementById(
        "checkout-items"
    );


const totalElement =
    document.getElementById(
        "checkout-total"
    );


const messageElement =
    document.getElementById(
        "checkout-message"
    );


// =========================================================
// دریافت سبد خرید از Backend
// =========================================================

async function getCheckoutCart() {

    const response =
        await fetch(
            "/api/orders/cart/"
        );


    if (!response.ok) {

        throw new Error(
            "Failed to load cart."
        );

    }


    return await response.json();
}


// =========================================================
// نمایش سبد خرید در Checkout
// =========================================================

async function renderCheckout() {

    try {

        const cart =
            await getCheckoutCart();


        // اگر سبد خالی باشد
        if (
            !cart.items ||
            cart.items.length === 0
        ) {

            itemsContainer.innerHTML = `
                <p>
                    Your cart is empty.
                </p>
            `;

            totalElement.textContent =
                "0 Toman";

            return;
        }


        // پاک کردن محتوای قبلی
        itemsContainer.innerHTML = "";


        // نمایش محصولات
        cart.items.forEach(item => {

            const itemElement =
                document.createElement(
                    "div"
                );


            itemElement.className =
                "checkout-item";


            itemElement.innerHTML = `
                <span>
                    ${item.title}
                    ×
                    ${item.quantity}
                </span>

                <strong>
                    ${formatPrice(item.item_total)}
                    Toman
                </strong>
            `;


            itemsContainer.appendChild(
                itemElement
            );

        });


        // نمایش مبلغ کل
        totalElement.textContent =
            `${formatPrice(cart.total)} Toman`;


    } catch (error) {

        console.error(
            "Checkout loading error:",
            error
        );


        messageElement.textContent =
            error.message;

    }

}


// =========================================================
// ثبت سفارش
// =========================================================

form.addEventListener(
    "submit",
    async event => {

        event.preventDefault();


        try {

            // دریافت سبد واقعی از Backend
            const cart =
                await getCheckoutCart();


            if (
                !cart.items ||
                cart.items.length === 0
            ) {

                throw new Error(
                    "Your cart is empty."
                );

            }


            const customerName =
                document
                    .getElementById(
                        "customer-name"
                    )
                    .value
                    .trim();


            if (!customerName) {

                throw new Error(
                    "Please enter your name or table number."
                );

            }


            // تبدیل آیتم‌های Cart API
            // به فرمت مورد نیاز Order API
            const items =
                cart.items.map(item => ({

                    product_id:
                        Number(
                            item.product_id
                        ),

                    quantity:
                        Number(
                            item.quantity
                        )

                }));


            // =================================================
            // مرحله اول:
            // ساخت سفارش در Backend
            // =================================================

            const orderResponse =
                await fetch(
                    "/api/orders/create/",
                    {
                        method: "POST",

                        headers: {
                            "Content-Type":
                                "application/json"
                        },

                        body: JSON.stringify({

                            customer_name:
                                customerName,

                            items:
                                items

                        })
                    }
                );


            const orderData =
                await orderResponse.json();


            if (!orderResponse.ok) {

                throw new Error(
                    orderData.detail ||
                    "Failed to create order."
                );

            }


            // =================================================
            // مرحله دوم:
            // شروع پرداخت
            // =================================================

            const paymentResponse =
                await fetch(
                    "/api/orders/payment/start/",
                    {
                        method: "POST",

                        headers: {
                            "Content-Type":
                                "application/json"
                        },

                        body: JSON.stringify({

                            order_code:
                                orderData.order_code

                        })
                    }
                );


            const paymentData =
                await paymentResponse.json();


            if (!paymentResponse.ok) {

                throw new Error(
                    paymentData.detail ||
                    "Failed to start payment."
                );

            }


            // =================================================
            // مرحله سوم:
            // انتقال به درگاه آزمایشی
            // =================================================

            window.location.href =
                paymentData.payment_url;


        } catch (error) {

            console.error(
                "Checkout error:",
                error
            );


            messageElement.textContent =
                error.message;

        }

    }
);


// =========================================================
// فرمت قیمت
// =========================================================

function formatPrice(price) {

    return Number(price)
        .toLocaleString("en-US");

}


// =========================================================
// اجرای Checkout
// =========================================================

document.addEventListener(
    "DOMContentLoaded",
    () => {

        renderCheckout();

    }
);
