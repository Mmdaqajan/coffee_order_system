// =========================================================
// تنظیمات API
// =========================================================

const ORDER_CREATE_API_URL = "/api/orders/create/";
const PAYMENT_CREATE_API_URL = "/api/orders/payment/create/";


// =========================================================
// اجرای صفحه بعد از لود کامل
// =========================================================

document.addEventListener("DOMContentLoaded", () => {
    loadCheckout();
});


// =========================================================
// دریافت سبد خرید از Backend
// =========================================================

async function loadCheckout() {

    try {

        const cart = await getCart();

        renderCheckout(cart);

    } catch (error) {

        console.error(
            "Checkout loading error:",
            error
        );

        showCheckoutError(
            "Failed to load your cart."
        );
    }
}


// =========================================================
// نمایش اطلاعات سبد در صفحه Checkout
// =========================================================

function renderCheckout(cart) {

    const loadingElement =
        document.getElementById("checkout-loading");

    const contentElement =
        document.getElementById("checkout-content");

    const itemsContainer =
        document.getElementById("checkout-items");

    const totalElement =
        document.getElementById("checkout-total");


    // مخفی کردن Loading
    loadingElement.style.display = "none";


    // بررسی خالی بودن سبد
    if (!cart.items || cart.items.length === 0) {

        showCheckoutError(
            "Your cart is empty."
        );

        return;
    }


    // نمایش صفحه Checkout
    contentElement.style.display = "block";


    // پاک کردن محصولات قبلی
    itemsContainer.innerHTML = "";


    // ساخت آیتم‌های سفارش
    cart.items.forEach(item => {

        const itemElement =
            createCheckoutItem(item);

        itemsContainer.appendChild(
            itemElement
        );

    });


    // نمایش مبلغ کل
    totalElement.textContent =
        `${formatPrice(cart.total)} Toman`;
}


// =========================================================
// ساخت یک آیتم سفارش
// =========================================================

function createCheckoutItem(item) {

    const element =
        document.createElement("div");

    element.className =
        "checkout-item";


    const image =
        item.image ||
        "/static/images/coffee.jpg";


    element.innerHTML = `
        <div class="checkout-item-image">
            <img
                src="${image}"
                alt="${item.title}"
                loading="lazy"
            >
        </div>

        <div class="checkout-item-info">

            <h3>
                ${item.title}
            </h3>

            <p>
                ${item.quantity}
                ×
                ${formatPrice(item.price)}
                Toman
            </p>

        </div>

        <strong>
            ${formatPrice(item.item_total)}
            Toman
        </strong>
    `;


    return element;
}


// =========================================================
// ثبت سفارش
// =========================================================

async function createOrder(customerName) {

    // ابتدا سبد واقعی Backend را دوباره می‌گیریم
    const cart = await getCart();


    if (!cart.items || cart.items.length === 0) {

        throw new Error(
            "Your cart is empty."
        );
    }


    // فقط ID و تعداد محصولات ارسال می‌شود.
    // قیمت از Frontend ارسال نمی‌شود.
    const items = cart.items.map(item => ({
        product_id: Number(item.product_id),
        quantity: Number(item.quantity)
    }));


    const response =
        await fetch(
            ORDER_CREATE_API_URL,
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


    const data =
        await response.json();


    if (!response.ok) {

        throw new Error(
            getApiErrorMessage(data)
        );
    }


    return data;
}


// =========================================================
// ایجاد پرداخت زرین‌پال
// =========================================================

async function createPayment(orderCode) {

    const response =
        await fetch(
            PAYMENT_CREATE_API_URL,
            {
                method: "POST",

                headers: {
                    "Content-Type":
                        "application/json"
                },

                body: JSON.stringify({
                    order_code:
                        orderCode
                })
            }
        );


    const data =
        await response.json();


    if (!response.ok) {

        throw new Error(
            getApiErrorMessage(data)
        );
    }


    return data;
}


// =========================================================
// ارسال فرم Checkout
// =========================================================

document.addEventListener(
    "DOMContentLoaded",
    () => {

        const form =
            document.getElementById(
                "checkout-form"
            );


        if (!form) {
            return;
        }


        form.addEventListener(
            "submit",
            handleCheckoutSubmit
        );

    }
);


// =========================================================
// مدیریت کلیک روی دکمه پرداخت
// =========================================================

async function handleCheckoutSubmit(event) {

    event.preventDefault();


    const form =
        event.currentTarget;


    const customerName =
        document.getElementById(
            "customer-name"
        ).value.trim();


    const paymentButton =
        document.getElementById(
            "payment-button"
        );


    // بررسی نام یا شماره میز
    if (!customerName) {

        showCheckoutError(
            "Please enter your name or table number."
        );

        return;
    }


    try {

        // -------------------------------------------------
        // غیرفعال کردن دکمه
        // -------------------------------------------------

        paymentButton.disabled = true;

        paymentButton.textContent =
            "Creating order...";


        // -------------------------------------------------
        // مرحله اول:
        // ساخت سفارش
        // -------------------------------------------------

        const order =
            await createOrder(
                customerName
            );


        // -------------------------------------------------
        // مرحله دوم:
        // ایجاد پرداخت
        // -------------------------------------------------

        paymentButton.textContent =
            "Connecting to ZarinPal...";


        const payment =
            await createPayment(
                order.order_code
            );


        // -------------------------------------------------
        // بررسی لینک پرداخت
        // -------------------------------------------------

        if (!payment.payment_url) {

            throw new Error(
                "Payment gateway URL was not received."
            );
        }


        // -------------------------------------------------
        // انتقال کاربر به زرین‌پال
        // -------------------------------------------------

        window.location.href =
            payment.payment_url;


    } catch (error) {

        console.error(
            "Payment error:",
            error
        );


        showCheckoutError(
            error.message
        );


        // فعال کردن مجدد دکمه
        paymentButton.disabled = false;

        paymentButton.textContent =
            "Proceed to Payment";
    }
}


// =========================================================
// نمایش خطای Checkout
// =========================================================

function showCheckoutError(message) {

    const loadingElement =
        document.getElementById(
            "checkout-loading"
        );

    const contentElement =
        document.getElementById(
            "checkout-content"
        );

    const errorElement =
        document.getElementById(
            "checkout-error"
        );

    const messageElement =
        document.getElementById(
            "checkout-error-message"
        );


    if (loadingElement) {

        loadingElement.style.display =
            "none";
    }


    if (contentElement) {

        contentElement.style.display =
            "none";
    }


    if (messageElement) {

        messageElement.textContent =
            message;
    }


    if (errorElement) {

        errorElement.style.display =
            "block";
    }
}


// =========================================================
// استخراج پیام خطا از API
// =========================================================

function getApiErrorMessage(data) {

    if (!data) {

        return "An unexpected error occurred.";
    }


    if (data.detail) {

        return data.detail;
    }


    // خطاهای Validation Serializer
    const firstKey =
        Object.keys(data)[0];


    if (firstKey) {

        const value =
            data[firstKey];


        if (Array.isArray(value)) {

            return value[0];
        }

        return String(value);
    }


    return "An unexpected error occurred.";
}


// =========================================================
// فرمت قیمت
// =========================================================

function formatPrice(price) {

    return Number(price)
        .toLocaleString("en-US");
}
