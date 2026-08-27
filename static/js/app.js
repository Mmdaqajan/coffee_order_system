document.addEventListener("DOMContentLoaded", () => {

    const productsContainer = document.getElementById("products-container");
    const categoriesContainer = document.querySelector(".category-list");

    let allProducts = [];


    // -----------------------------
    // Fetch menu from Django API
    // -----------------------------

    async function loadMenu() {

        try {

            const response = await fetch("/api/menu/");

            if (!response.ok) {
                throw new Error(`HTTP error: ${response.status}`);
            }

            const categories = await response.json();

            allProducts = [];

            categories.forEach(category => {

                category.products.forEach(product => {

                    allProducts.push({
                        ...product,
                        categoryTitle: category.title
                    });

                });

            });

            renderCategories(categories);
            renderProducts(allProducts);

        } catch (error) {

            console.error("Failed to load menu:", error);

            productsContainer.innerHTML = `
                <p class="error">
                    Failed to load menu. Please try again.
                </p>
            `;
        }
    }


    // -----------------------------
    // Render categories
    // -----------------------------

    function renderCategories(categories) {

        categoriesContainer.innerHTML = `
            <button class="category active" data-category="all">
                All
            </button>
        `;

        categories.forEach(category => {

            const button = document.createElement("button");

            button.className = "category";

            button.dataset.category = category.id;

            button.textContent = category.title;

            categoriesContainer.appendChild(button);
        });


        // Category click

        const categoryButtons =
            document.querySelectorAll(".category");

        categoryButtons.forEach(button => {

            button.addEventListener("click", () => {

                categoryButtons.forEach(item => {
                    item.classList.remove("active");
                });

                button.classList.add("active");

                const categoryId = button.dataset.category;

                if (categoryId === "all") {

                    renderProducts(allProducts);

                } else {

                    const filteredProducts =
                        allProducts.filter(
                            product =>
                                String(product.category) ===
                                String(categoryId)
                        );

                    renderProducts(filteredProducts);
                }
            });
        });
    }


    // -----------------------------
    // Render products
    // -----------------------------

   

    // -----------------------------
    // Add button
    // -----------------------------

    function attachAddButtons() {

        const buttons =
            document.querySelectorAll(".add-button");


        buttons.forEach(button => {

            button.addEventListener("click", () => {

                const productId =
                    button.dataset.productId;

                console.log(
                    "Product added:",
                    productId
                );


                button.textContent = "✓";


                setTimeout(() => {
                    button.textContent = "+";
                }, 800);

            });

        });
    }


    // -----------------------------
    // Format price
    // -----------------------------

    function formatPrice(price) {

        return Number(price).toLocaleString("en-US");
    }


    // -----------------------------
    // Basic HTML escaping
    // -----------------------------

    // function escapeHTML(value) {

    //     const div = document.createElement("div");

    //     div.textContent = value;

    //     return div.innerHTML;
    // }


    // Start
// codes to load products by filter without reloading the page
const categoryLinks =document.querySelectorAll(".category");

const productsContainer2 =document.getElementById("products-container");


categoryLinks.forEach(link => {

    link.addEventListener("click", async event => {

        event.preventDefault();

        categoryLinks.forEach(item => {
            item.classList.remove("active");
        });

        link.classList.add("active");


        const url = new URL(
            link.href,
            window.location.origin
        );

        const category =
            url.searchParams.get("category");


        const endpoint = category
            ? `/products/?category=${category}`
            : "/products/";


        try {

            const response =
                await fetch(endpoint);

            if (!response.ok) {
                throw new Error("Request failed");
            }

            const html =
                await response.text();

            productsContainer2.innerHTML = html;

        } catch (error) {

            console.error(error);

        }

    });

});

let cart = JSON.parse(
    localStorage.getItem("cart") || "{}"
);


function saveCart() {
    localStorage.setItem(
        "cart",
        JSON.stringify(cart)
    );
}


function updateCartUI() {

    let count = 0;
    let total = 0;

    const cartItems =
        document.getElementById("cart-items");

    cartItems.innerHTML = "";

    Object.values(cart).forEach(item => {

        count += item.quantity;
        total += item.price * item.quantity;

        const itemElement =
            document.createElement("div");

        itemElement.className = "cart-item";

        itemElement.innerHTML = `
            <span>${item.title}</span>

            <div>
                <button
                    class="cart-minus"
                    data-id="${item.id}"
                >
                    −
                </button>

                <span>${item.quantity}</span>

                <button
                    class="cart-plus"
                    data-id="${item.id}"
                >
                    +
                </button>
            </div>

            <strong>
                ${(item.price * item.quantity)
                    .toLocaleString("fa-IR")}
                تومان
            </strong>
        `;

        cartItems.appendChild(itemElement);
    });

    document.getElementById("cart-count").textContent =
        count;

    document.getElementById("cart-total").textContent =
        total.toLocaleString("fa-IR");
}


document.addEventListener("click", event => {


    const plus =
        event.target.closest(".cart-plus");

    const minus =
        event.target.closest(".cart-minus");


    if (plus) {

        const id = plus.dataset.id;

        cart[id].quantity++;

        saveCart();
        updateCartUI();
    }


    if (minus) {

        const id = minus.dataset.id;

        cart[id].quantity--;

        if (cart[id].quantity <= 0) {
            delete cart[id];
        }

        saveCart();
        updateCartUI();
    }

    const button =
        event.target.closest(".add-button");

    if (!button) return;

    const id =
        button.dataset.productId;

    const title =
        button.dataset.productTitle;

    const price =
        Number(button.dataset.productPrice);


    if (!cart[id]) {

        cart[id] = {
            id: id,
            title: title,
            price: price,
            quantity: 1
        };

    } else {

        cart[id].quantity++;

    }


    saveCart();
    updateCartUI();

});


updateCartUI();

});