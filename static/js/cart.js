const cartPageItems =
    document.getElementById("cart-page-items");

const cartEmpty =
    document.getElementById("cart-empty");

const cartCheckout =
    document.getElementById("cart-checkout");

const pageCartTotal =
    document.getElementById("page-cart-total");


let cart = JSON.parse(
    localStorage.getItem("cart") || "{}"
);


function saveCart() {

    localStorage.setItem(
        "cart",
        JSON.stringify(cart)
    );

}


function renderCart() {

    cartPageItems.innerHTML = "";

    const items =
        Object.values(cart);


    if (items.length === 0) {

        cartEmpty.style.display = "block";
        cartCheckout.style.display = "none";

        return;
    }


    cartEmpty.style.display = "none";
    cartCheckout.style.display = "block";


    let total = 0;


    items.forEach(item => {

        const itemTotal =
            item.price * item.quantity;

        total += itemTotal;


        const element =
            document.createElement("div");

        element.className = "cart-page-item";


        element.innerHTML = `

            <div class="cart-item-info">

                <h3>
                    ${item.title}
                </h3>

                <span>
                    ${item.price.toLocaleString("fa-IR")}
                    تومان
                </span>

            </div>


            <div class="cart-item-controls">

                <button
                    class="cart-page-plus"
                    data-id="${item.id}"
                >
                    +
                </button>

                <span>
                    ${item.quantity}
                </span>

                <button
                    class="cart-page-minus"
                    data-id="${item.id}"
                >
                    −
                </button>

            </div>


            <strong>

                ${itemTotal.toLocaleString("fa-IR")}

                تومان

            </strong>

        `;


        cartPageItems.appendChild(element);

    });


    pageCartTotal.textContent =
        `${total.toLocaleString("fa-IR")} تومان`;

}


document.addEventListener(
    "click",
    event => {

        const plus =
            event.target.closest(
                ".cart-page-plus"
            );

        const minus =
            event.target.closest(
                ".cart-page-minus"
            );


        if (plus) {

            const id =
                plus.dataset.id;

            cart[id].quantity++;

            saveCart();
            renderCart();

        }


        if (minus) {

            const id =
                minus.dataset.id;

            cart[id].quantity--;


            if (cart[id].quantity <= 0) {

                delete cart[id];

            }


            saveCart();
            renderCart();

        }

    }
);


renderCart();