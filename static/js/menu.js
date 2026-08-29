//javascript
// =========================================================
// اجرای اولیه صفحه بعد از کامل شدن HTML
// =========================================================

document.addEventListener(
    "DOMContentLoaded",
    () => {
        loadMenu();

        // خلاصه سبد خرید را هم از API می‌گیریم
        updateCartSummary();
    }
);


// =========================================================
// تصاویر پیش‌فرض دسته‌بندی‌ها
// اگر محصول عکس نداشته باشد، عکس دسته‌بندی نمایش داده می‌شود.
// =========================================================

const categoryImages = {

    1: "/static/images/cold-bar.jpg",

    2: "/static/images/hot-bar.jpg",

    3: "/static/images/coffee.jpg",

    4: "/static/images/cake.jpg",

};


// =========================================================
// دریافت منو از API
// =========================================================

async function loadMenu() {

    const categoryContainer =
        document.getElementById(
            "category-list"
        );


    const productsContainer =
        document.getElementById(
            "products-container"
        );


    try {

        // درخواست دریافت دسته‌بندی‌ها و محصولات
        const response =
            await fetch(
                "/api/menu/"
            );


        // بررسی موفق بودن درخواست
        if (!response.ok) {

            throw new Error(
                `HTTP error: ${response.status}`
            );

        }


        // تبدیل پاسخ API به JSON
        const categories =
            await response.json();


        // نمایش دسته‌بندی‌ها
        renderCategories(
            categories,
            categoryContainer,
            productsContainer
        );


        // تبدیل محصولات تمام دسته‌بندی‌ها
        // به یک آرایه واحد
        const products =
            getAllProducts(
                categories
            );


        // نمایش تمام محصولات
        renderProducts(
            products,
            productsContainer
        );


    } catch (error) {

        console.error(
            "Menu loading error:",
            error
        );


        productsContainer.innerHTML = `
            <p class="error-message">
                Failed to load products.
            </p>
        `;

    }

}


// =========================================================
// استخراج تمام محصولات از تمام دسته‌بندی‌ها
// =========================================================

function getAllProducts(categories) {

    return categories.flatMap(
        category => {

            return category.products.map(
                product => ({

                    ...product,

                    // ذخیره ID دسته‌بندی
                    // برای انتخاب عکس پیش‌فرض
                    category_id:
                        category.id,

                })
            );

        }
    );

}


// =========================================================
// نمایش دسته‌بندی‌ها
// =========================================================

function renderCategories(
    categories,
    container,
    productsContainer
) {

    // پاک کردن محتوای قبلی
    container.innerHTML = "";


    // -----------------------------------------------------
    // دکمه All
    // -----------------------------------------------------

    const allButton =
        document.createElement(
            "button"
        );


    allButton.type = "button";

    allButton.className =
        "category active";

    allButton.textContent =
        "All";


    allButton.addEventListener(
        "click",
        () => {

            // فعال کردن دکمه All
            setActiveCategory(
                allButton
            );


            // نمایش تمام محصولات
            renderProducts(
                getAllProducts(
                    categories
                ),
                productsContainer
            );

        }
    );


    container.appendChild(
        allButton
    );


    // -----------------------------------------------------
    // ساخت دکمه هر دسته‌بندی
    // -----------------------------------------------------

    categories.forEach(
        category => {

            const button =
                document.createElement(
                    "button"
                );


            button.type = "button";

            button.className =
                "category";

            button.textContent =
                category.title;


            button.addEventListener(
                "click",
                () => {

                    // فعال کردن دسته انتخاب‌شده
                    setActiveCategory(
                        button
                    );


                    // فقط محصولات همین دسته‌بندی
                    const products =
                        category.products.map(
                            product => ({

                                ...product,

                                category_id:
                                    category.id,

                            })
                        );


                    // نمایش محصولات
                    renderProducts(
                        products,
                        productsContainer
                    );

                }
            );


            container.appendChild(
                button
            );

        }
    );

}


// =========================================================
// تغییر دسته‌بندی فعال
// =========================================================

function setActiveCategory(
    activeButton
) {

    // حذف active از تمام دکمه‌ها
    document
        .querySelectorAll(
            ".category"
        )
        .forEach(
            button => {

                button.classList.remove(
                    "active"
                );

            }
        );


    // فعال کردن دکمه انتخاب‌شده
    activeButton.classList.add(
        "active"
    );

}


// =========================================================
// نمایش محصولات
// =========================================================

function renderProducts(
    products,
    container
) {

    // ذخیره محصولات فعلی در صورت نیاز
    window.currentMenuProducts =
        products;


    // پاک کردن محصولات قبلی
    container.innerHTML = "";


    // اگر محصولی وجود نداشت
    if (!products.length) {

        container.innerHTML = `
            <div class="empty-products">

                <p>
                    No products available.
                </p>

            </div>
        `;

        return;

    }


    // -----------------------------------------------------
    // ساخت کارت هر محصول
    // -----------------------------------------------------

    products.forEach(
        product => {

            const card =
                document.createElement(
                    "article"
                );


            card.className =
                "product-card";


            // اگر محصول عکس داشته باشد
            // همان عکس استفاده می‌شود.
            //
            // اگر عکس نداشته باشد
            // عکس پیش‌فرض دسته‌بندی استفاده می‌شود.
            const image =
                product.image ||
                categoryImages[
                    product.category_id
                ];


            card.innerHTML = `

                <div class="product-image">

                    ${
                        image
                            ? `
                                <img
                                    src="${image}"
                                    alt="${product.title}"
                                    loading="lazy"

                                    onerror="
                                        this.parentElement.innerHTML =
                                        '<div class=&quot;product-image-placeholder&quot;>☕</div>'
                                    "
                                >
                            `
                            : `
                                <div
                                    class="product-image-placeholder"
                                >
                                    ☕
                                </div>
                            `
                    }

                </div>


                <div class="product-info">

                    <h3>
                        ${product.title}
                    </h3>


                    ${
                        product.description
                            ? `
                                <p>
                                    ${product.description}
                                </p>
                            `
                            : `
                                <p
                                    class="no-description"
                                >
                                    Freshly prepared
                                    for you.
                                </p>
                            `
                    }


                    <div class="product-bottom">

                        <strong>
                            ${formatPrice(
                                product.price
                            )}
                            Toman
                        </strong>


                        <!--
                            ID محصول داخل data-product-id
                            قرار می‌گیرد تا هنگام کلیک
                            آن را به API ارسال کنیم.
                        -->

                        <button
                            type="button"
                            class="add-to-cart"
                            data-product-id="${product.id}"
                        >
                            + Add
                        </button>

                    </div>

                </div>

            `;


            container.appendChild(
                card
            );

        }
    );


    // فعال کردن تمام دکمه‌های Add
    // بعد از ساخته شدن کارت‌ها
    attachAddToCartButtons();

}


// =========================================================
// فعال کردن دکمه‌های Add to Cart
// =========================================================

function attachAddToCartButtons() {

    // پیدا کردن تمام دکمه‌های Add
    const buttons =
        document.querySelectorAll(
            ".add-to-cart"
        );


    buttons.forEach(
        button => {

            button.addEventListener(
                "click",
                async () => {

                    // گرفتن ID محصول از HTML
                    const productId =
                        Number(
                            button.dataset.productId
                        );


                    try {

                        // ارسال محصول به API سبد خرید
                        await addToCart(
                            productId,
                            1
                        );


                        // نمایش موفقیت موقت
                        button.textContent =
                            "✓ Added";


                        // جلوگیری از چند کلیک
                        // پشت سر هم در همان لحظه
                        button.disabled =
                            true;


                        // دریافت تعداد و مبلغ جدید
                        // از API
                        await updateCartSummary();


                        // بعد از مدت کوتاه
                        // دکمه دوباره فعال شود
                        setTimeout(
                            () => {

                                button.textContent =
                                    "+ Add";

                                button.disabled =
                                    false;

                            },
                            700
                        );


                    } catch (error) {

                        console.error(
                            "Add to cart error:",
                            error
                        );


                        alert(
                            "Failed to add product."
                        );

                    }

                }
            );

        }
    );

}


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

