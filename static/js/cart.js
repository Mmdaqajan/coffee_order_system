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


    Object.values(cart).forEach(
        item => {

            count += item.quantity;

            total +=
                item.price *
                item.quantity;

        }
    );


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
            count;

    }


    if (totalElement) {

        totalElement.textContent =
            total.toLocaleString(
                "fa-IR"
            );

    }
}


document.addEventListener(
    "click",
    event => {

        const button =
            event.target.closest(
                ".add-button"
            );


        if (!button) {
            return;
        }


        const id =
            button.dataset.productId;


        const title =
            button.dataset.productTitle;


        const price =
            Number(
                button.dataset.productPrice
            );


        if (!cart[id]) {

            cart[id] = {

                id,

                title,

                price,

                quantity: 1

            };

        } else {

            cart[id].quantity++;

        }


        saveCart();

        updateCartUI();

    }
);


updateCartUI();