const API_URL = "/api/menu/";

const categoryList =
    document.getElementById("category-list");

const productsContainer =
    document.getElementById(
        "products-container"
    );


async function loadMenu(categoryId = null) {

    productsContainer.innerHTML = `
        <p>در حال دریافت محصولات...</p>
    `;


    let url = API_URL;


    if (categoryId) {

        url += `?category=${categoryId}`;

    }


    try {

        const response =
            await fetch(url);


        if (!response.ok) {

            throw new Error(
                "Failed to load menu"
            );

        }


        const categories =
            await response.json();


        renderCategories(categories);

        renderProducts(categories);


    } catch (error) {

        console.error(error);

        productsContainer.innerHTML = `
            <p>
                دریافت محصولات با مشکل مواجه شد.
            </p>
        `;
    }
}


function renderCategories(categories) {

    categoryList.innerHTML = "";


    const allButton =
        document.createElement("button");

    allButton.className =
        "category active";

    allButton.textContent =
        "همه";


    allButton.addEventListener(
        "click",
        () => {

            setActiveCategory(
                allButton
            );

            loadMenu();

        }
    );


    categoryList.appendChild(
        allButton
    );


    categories.forEach(category => {

        const button =
            document.createElement(
                "button"
            );


        button.className =
            "category";


        button.textContent =
            category.title;


        button.dataset.categoryId =
            category.id;


        button.addEventListener(
            "click",
            () => {

                setActiveCategory(
                    button
                );

                loadMenu(
                    category.id
                );

            }
        );


        categoryList.appendChild(
            button
        );

    });
}


function renderProducts(categories) {

    productsContainer.innerHTML = "";


    let products = [];


    categories.forEach(category => {

        category.products.forEach(
            product => {

                products.push({
                    ...product,

                    category_title:
                        category.title
                });

            }
        );

    });


    if (products.length === 0) {

        productsContainer.innerHTML = `
            <p>
                محصولی یافت نشد.
            </p>
        `;

        return;
    }


    products.forEach(product => {

        const card =
            document.createElement(
                "article"
            );


        card.className =
            "product-card";


        const image =
            product.image
                ? `
                    <img
                        src="${product.image}"
                        alt="${product.title}"
                    >
                  `
                : `
                    <div class="no-image">
                        ☕
                    </div>
                  `;


        card.innerHTML = `

            <div class="product-image">

                ${image}

            </div>


            <div class="product-info">

                <div class="product-header">

                    <h3>
                        ${product.title}
                    </h3>

                    <span>
                        ${product.category_title}
                    </span>

                </div>


                <p class="product-description">

                    ${product.description || ""}

                </p>


                <div class="product-footer">

                    <span class="product-price">

                        ${Number(
                            product.price
                        ).toLocaleString("fa-IR")}

                        تومان

                    </span>


                    <button
                        class="add-button"
                        data-product-id="${product.id}"
                        data-product-title="${product.title}"
                        data-product-price="${product.price}"
                    >
                        +
                    </button>

                </div>

            </div>
        `;


        productsContainer.appendChild(
            card
        );

    });
}


function setActiveCategory(button) {

    document
        .querySelectorAll(".category")
        .forEach(item => {

            item.classList.remove(
                "active"
            );

        });


    button.classList.add(
        "active"
    );
}