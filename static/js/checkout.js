//javascript
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

async function loadCheckoutCart() {

    try {

        // دریافت سبد خرید واقعی از API
        const response =
            await fetch(
                "/api/orders/cart/"
            );


        if (!response.ok) {

            throw new Error(
                "Failed to load cart."
            );

        }


        const cart =
            await response.json();


        // نمایش اطلاعات سبد
        renderCheckout(
            cart
        );


    } catch (error) {

        console.error(
            "Checkout cart error:",
            error
        );


        itemsContainer.innerHTML = `
            <p>
                Failed to load cart.
            </p>
        `;

    }

}


// =========================================================
// نمایش محصولات در صفحه Checkout
// =========================================================

function renderCheckout(cart) {

    // اگر سبد خالی باشد
    if (
        !cart.items ||
        cart.items.length === 0
    ) {

        itemsContainer.innerHTML = `
            <p>
                سبد خرید خالی است.
            </p>
        `;


        totalElement.textContent =
            "0 تومان";


        // غیرفعال کردن دکمه ثبت سفارش
        const submitButton =
            form.querySelector(
                'button[type="submit"]'
            );


        if (submitButton) {
            submitButton.disabled = true;
        }


        return;
    }


    // فعال بودن دکمه ثبت سفارش
    const submitButton =
        form.querySelector(
            'button[type="submit"]'
        );


    if (submitButton) {
        submitButton.disabled = false;
    }


    // پاک کردن محصولات قبلی
    itemsContainer.innerHTML = "";


    // نمایش محصولات
    cart.items.forEach(
        item => {

            itemsContainer.innerHTML += `

                <div class="checkout-item">

                    <span>
                        ${item.title}
                    </span>

                    <span>
                        ${item.quantity}
                        ×
                        ${formatPrice(item.price)}
                    </span>

                </div>

            `;

        }
    );


    // نمایش مبلغ کل که از Backend آمده است
    totalElement.textContent =
        `${formatPrice(cart.total)} تومان`;

}


// =========================================================
// ثبت سفارش
// =========================================================

form.addEventListener(
    "submit",
    async event => {

        event.preventDefault();


        // دریافت نام مشتری
        const customerName =
            document.getElementById(
                "customer-name"
            ).value.trim();


        // بررسی نام مشتری
        if (!customerName) {

            messageElement.textContent =
                "لطفاً نام یا شماره میز را وارد کنید.";

            return;

        }


        try {

            // ابتدا سبد فعلی را از Backend می‌گیریم
            const cartResponse =
                await fetch(
                    "/api/orders/cart/"
                );


            if (!cartResponse.ok) {

                throw new Error(
                    "Failed to load cart."
                );

            }


            const cart =
                await cartResponse.json();


            // بررسی خالی نبودن سبد
            if (
                !cart.items ||
                cart.items.length === 0
            ) {

                throw new Error(
                    "سبد خرید شما خالی است."
                );

            }


            // تبدیل اطلاعات سبد به فرمت مورد نیاز API سفارش
            const items =
                cart.items.map(
                    item => ({

                        product_id:
                            Number(
                                item.product_id
                            ),

                        quantity:
                            Number(
                                item.quantity
                            )

                    })
                );


            // ارسال سفارش به Backend
            const response =
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


            // دریافت پاسخ Backend
            const data =
                await response.json();


            // بررسی خطای API
            if (!response.ok) {

                throw new Error(
                    data.detail ||
                    "ثبت سفارش ناموفق بود."
                );

            }


            // سفارش با موفقیت ثبت شده است.
            // سبد Session را Backend باید
            // بعد از ثبت سفارش پاک کند.


            // انتقال به صفحه موفقیت سفارش
            window.location.href =
                `/order-success/?code=${data.order_code}`;


        } catch (error) {

            console.error(
                "Order creation error:",
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

    return Number(
        price
    ).toLocaleString(
        "en-US"
    );

}


// =========================================================
// اجرای اولیه صفحه
// =========================================================

document.addEventListener(
    "DOMContentLoaded",
    () => {

        loadCheckoutCart();

    }
);

