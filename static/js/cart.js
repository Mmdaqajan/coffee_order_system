// =========================================================
// تنظیمات API سبد خرید
// =========================================================

const CART_API_URL = "/api/orders/cart/";


// =========================================================
// دریافت سبد خرید از Backend
// =========================================================

async function getCart() {

    const response =
        await fetch(CART_API_URL);


    if (!response.ok) {

        throw new Error(
            "Failed to load cart."
        );

    }


    return await response.json();
}


// =========================================================
// اضافه کردن محصول به سبد خرید
// =========================================================

async function addToCart(
    productId,
    quantity = 1
) {

    const response =
        await fetch(
            "/api/orders/cart/add/",
            {
                method: "POST",

                headers: {
                    "Content-Type":
                        "application/json"
                },

                body: JSON.stringify({
                    product_id:
                        productId,

                    quantity:
                        quantity
                })
            }
        );


    if (!response.ok) {

        let errorMessage =
            "Failed to add product.";

        try {

            const error =
                await response.json();

            errorMessage =
                error.detail ||
                errorMessage;

        } catch (error) {
            // اگر پاسخ JSON نبود،
            // همان پیام پیش‌فرض نمایش داده می‌شود.
        }


        throw new Error(
            errorMessage
        );

    }


    const cart =
        await response.json();


    // بعد از اضافه شدن محصول،
    // خلاصه سبد را از Backend به‌روز می‌کنیم.
    await updateCartSummary();


    return cart;
}


// =========================================================
// تغییر تعداد محصول
// =========================================================

async function updateCartItem(
    productId,
    quantity
) {

    // جلوگیری از ارسال تعداد نامعتبر
    if (quantity < 1) {

        return;

    }


    const response =
        await fetch(
            "/api/orders/cart/update/",
            {
                method: "PATCH",

                headers: {
                    "Content-Type":
                        "application/json"
                },

                body: JSON.stringify({
                    product_id:
                        productId,

                    quantity:
                        quantity
                })
            }
        );


    if (!response.ok) {

        let errorMessage =
            "Failed to update cart.";

        try {

            const error =
                await response.json();

            errorMessage =
                error.detail ||
                errorMessage;

        } catch (error) {
            // پاسخ غیر JSON
        }


        throw new Error(
            errorMessage
        );

    }


    return await response.json();
}


// =========================================================
// حذف محصول از سبد خرید
// =========================================================

async function removeCartItem(
    productId
) {

    const response =
        await fetch(
            "/api/orders/cart/remove/",
            {
                method: "DELETE",

                headers: {
                    "Content-Type":
                        "application/json"
                },

                body: JSON.stringify({
                    product_id:
                        productId
                })
            }
        );


    if (!response.ok) {

        let errorMessage =
            "Failed to remove product.";

        try {

            const error =
                await response.json();

            errorMessage =
                error.detail ||
                errorMessage;

        } catch (error) {
            // پاسخ غیر JSON
        }


        throw new Error(
            errorMessage
        );

    }


    return await response.json();
}


// =========================================================
// خالی کردن کامل سبد خرید
// =========================================================

async function clearCart() {

    const response =
        await fetch(
            "/api/orders/cart/clear/",
            {
                method: "DELETE"
            }
        );


    if (!response.ok) {

        let errorMessage =
            "Failed to clear cart.";

        try {

            const error =
                await response.json();

            errorMessage =
                error.detail ||
                errorMessage;

        } catch (error) {
            // پاسخ غیر JSON
        }


        throw new Error(
            errorMessage
        );

    }


    return await response.json();
}


// =========================================================
// به‌روزرسانی خلاصه سبد در هدر
// =========================================================

async function updateCartSummary() {

    try {

        const cart =
            await getCart();


        const countElement =
            document.getElementById(
                "cart-count"
            );


        const totalElement =
            document.getElementById(
                "cart-total"
            );


        if (countElement) {

            countElement.textContent =
                cart.count;

        }


        if (totalElement) {

            totalElement.textContent =
                formatPrice(
                    cart.total
                );

        }

    } catch (error) {

        console.error(
            "Cart summary error:",
            error
        );

    }
}


// =========================================================
// بارگذاری صفحه Cart
// =========================================================

async function loadCartPage() {

    const loadingContainer =
        document.getElementById(
            "cart-loading"
        );


    const itemsContainer =
        document.getElementById(
            "cart-page-items"
        );


    // اگر این صفحه Cart نیست،
    // تابع متوقف می‌شود.
    if (!itemsContainer) {

        return;

    }


    try {

        // دریافت مستقیم اطلاعات از Backend
        const cart =
            await getCart();


        // مخفی کردن Loading
        if (loadingContainer) {

            loadingContainer.style.display =
                "none";

        }


        // نمایش اطلاعات سبد
        renderCart(cart);


    } catch (error) {

        console.error(
            "Cart loading error:",
            error
        );


        if (loadingContainer) {

            loadingContainer.style.display =
                "none";

        }


        itemsContainer.innerHTML = `
            <div class="cart-error">

                <p>
                    Failed to load cart.
                </p>

                <button
                    type="button"
                    id="retry-cart"
                >
                    Try Again
                </button>

            </div>
        `;


        const retryButton =
            document.getElementById(
                "retry-cart"
            );


        if (retryButton) {

            retryButton.addEventListener(
                "click",
                loadCartPage
            );

        }

    }
}


// =========================================================
// نمایش اطلاعات سبد خرید
// =========================================================

function renderCart(cart) {

    const itemsContainer =
        document.getElementById(
            "cart-page-items"
        );


    const emptyContainer =
        document.getElementById(
            "cart-empty"
        );


    const checkoutContainer =
        document.getElementById(
            "cart-checkout"
        );


    const totalElement =
        document.getElementById(
            "page-cart-total"
        );


    const countElement =
        document.getElementById(
            "page-cart-count"
        );


    if (!itemsContainer) {

        return;

    }


    // نمایش تعداد کل محصولات
    if (countElement) {

        countElement.textContent =
            cart.count || 0;

    }


    // نمایش مبلغ کل
    if (totalElement) {

        totalElement.textContent =
            `${formatPrice(cart.total || 0)} Toman`;

    }


    // =====================================================
    // بررسی خالی بودن سبد
    // =====================================================

    if (
        !cart.items ||
        cart.items.length === 0
    ) {

        itemsContainer.innerHTML = "";


        if (emptyContainer) {

            emptyContainer.style.display =
                "block";

        }


        if (checkoutContainer) {

            checkoutContainer.style.display =
                "none";

        }


        return;

    }


    // =====================================================
    // سبد دارای محصول است
    // =====================================================

    if (emptyContainer) {

        emptyContainer.style.display =
            "none";

    }


    if (checkoutContainer) {

        checkoutContainer.style.display =
            "block";

    }


    // پاک کردن محصولات قبلی
    itemsContainer.innerHTML = "";


    // ساخت محصولات
    cart.items.forEach(
        item => {

            const itemElement =
                createCartItem(item);


            itemsContainer.appendChild(
                itemElement
            );

        }
    );
}


// =========================================================
// ساخت کارت یک محصول
// =========================================================

function createCartItem(item) {

    const element =
        document.createElement(
            "article"
        );


    element.className =
        "cart-item";


    // اگر محصول عکس نداشت،
    // عکس پیش‌فرض استفاده می‌شود.
    const image =
        item.image ||
        "/static/images/coffee.jpg";


    element.innerHTML = `

        <div class="cart-item-image">

            <img
                src="${image}"
                alt="${item.title}"
                loading="lazy"
                onerror="
                    this.src='/static/images/coffee.jpg'
                "
            >

        </div>


        <div class="cart-item-info">

            <h3>
                ${item.title}
            </h3>


            <p class="cart-item-price">

                ${formatPrice(item.price)}
                Toman

            </p>


            <div class="cart-item-controls">

                <button
                    type="button"
                    class="quantity-button"
                    data-action="decrease"
                >
                    −
                </button>


                <span class="cart-item-quantity">

                    ${item.quantity}

                </span>


                <button
                    type="button"
                    class="quantity-button"
                    data-action="increase"
                >
                    +
                </button>

            </div>


            <button
                type="button"
                class="remove-cart-item"
            >
                Remove
            </button>

        </div>


        <strong class="cart-item-total">

            ${formatPrice(item.item_total)}
            Toman

        </strong>

    `;


    // فعال کردن + و -
    setupQuantityButtons(
        element,
        item
    );


    // فعال کردن Remove
    setupRemoveButton(
        element,
        item
    );


    return element;
}


// =========================================================
// مدیریت + و -
// =========================================================

function setupQuantityButtons(
    element,
    item
) {

    const buttons =
        element.querySelectorAll(
            ".quantity-button"
        );


    buttons.forEach(
        button => {

            button.addEventListener(
                "click",
                async () => {

                    let newQuantity =
                        item.quantity;


                    // افزایش تعداد
                    if (
                        button.dataset.action ===
                        "increase"
                    ) {

                        newQuantity++;

                    }


                    // کاهش تعداد
                    if (
                        button.dataset.action ===
                        "decrease"
                    ) {

                        newQuantity--;

                    }


                    // اگر تعداد به صفر برسد،
                    // محصول حذف می‌شود.
                    if (
                        newQuantity <= 0
                    ) {

                        try {

                            await removeCartItem(
                                item.product_id
                            );


                            await loadCartPage();


                            await updateCartSummary();

                        } catch (error) {

                            console.error(
                                "Remove error:",
                                error
                            );

                            alert(
                                error.message
                            );

                        }


                        return;

                    }


                    try {

                        // ارسال تعداد جدید به Backend
                        await updateCartItem(
                            item.product_id,
                            newQuantity
                        );


                        // دریافت مجدد سبد از Backend
                        await loadCartPage();


                        // به‌روزرسانی Header
                        await updateCartSummary();

                    } catch (error) {

                        console.error(
                            "Quantity update error:",
                            error
                        );


                        alert(
                            error.message
                        );

                    }

                }
            );

        }
    );
}


// =========================================================
// حذف محصول
// =========================================================

function setupRemoveButton(
    element,
    item
) {

    const button =
        element.querySelector(
            ".remove-cart-item"
        );


    if (!button) {

        return;

    }


    button.addEventListener(
        "click",
        async () => {

            try {

                // حذف از Backend
                await removeCartItem(
                    item.product_id
                );


                // دریافت مجدد اطلاعات
                await loadCartPage();


                // آپدیت خلاصه Header
                await updateCartSummary();

            } catch (error) {

                console.error(
                    "Remove cart item error:",
                    error
                );


                alert(
                    error.message
                );

            }

        }
    );
}


// =========================================================
// فرمت قیمت
// =========================================================

function formatPrice(price) {

    return Number(price || 0)
        .toLocaleString("en-US");

}


// =========================================================
// اجرای خودکار
// =========================================================

document.addEventListener(
    "DOMContentLoaded",
    () => {

        // اگر صفحه Cart باشد،
        // اطلاعات را از API می‌گیریم.
        if (
            document.getElementById(
                "cart-page-items"
            )
        ) {

            loadCartPage();

        }


        // اگر Header سبد وجود داشته باشد،
        // خلاصه آن از API خوانده می‌شود.
        if (
            document.getElementById(
                "cart-count"
            ) ||
            document.getElementById(
                "cart-total"
            )
        ) {

            updateCartSummary();

        }

    }
);

