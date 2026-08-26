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

    function escapeHTML(value) {

        const div = document.createElement("div");

        div.textContent = value;

        return div.innerHTML;
    }


    // Start


});