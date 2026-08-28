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


let cart = JSON.parse(
    localStorage.getItem("cart") || "{}"
);


function renderCheckout() {

    const items =
        Object.values(cart);


    if (!items.length) {

        itemsContainer.innerHTML = `
            <p>
                سبد خرید خالی است.
            </p>
        `;

        return;
    }


    let total = 0;


    itemsContainer.innerHTML = "";


    items.forEach(item => {

        const itemTotal =
            item.price *
            item.quantity;


        total += itemTotal;


        itemsContainer.innerHTML += `

            <div class="checkout-item">

                <span>
                    ${item.title}
                </span>

                <span>
                    ${item.quantity}
                    ×
                    ${item.price.toLocaleString("fa-IR")}
                </span>

            </div>

        `;

    });


    totalElement.textContent =
        `${total.toLocaleString("fa-IR")} تومان`;
}


form.addEventListener(
    "submit",
    async event => {

        event.preventDefault();


        const customerName =
            document.getElementById(
                "customer-name"
            ).value.trim();


        const items =
            Object.values(cart).map(
                item => ({

                    product_id:
                        Number(item.id),

                    quantity:
                        item.quantity

                })
            );


        try {

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


            const data =
                await response.json();


            if (!response.ok) {

                throw new Error(
                    data.detail ||
                    "ثبت سفارش ناموفق بود."
                );
            }


            localStorage.removeItem(
                "cart"
            );


            window.location.href =
                `/order-success/?code=${data.order_code}`;

        } catch (error) {

            messageElement.textContent =
                error.message;

        }

    }
);


renderCheckout();