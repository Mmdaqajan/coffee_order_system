let cart = JSON.parse(
    localStorage.getItem("cart") || "{}"
);


const form =
    document.getElementById("checkout-form");

const itemsContainer =
    document.getElementById("checkout-items");

const totalElement =
    document.getElementById("checkout-total");

const messageElement =
    document.getElementById("checkout-message");

const submitButton =
    document.getElementById("submit-order");


function renderCheckout() {

    itemsContainer.innerHTML = "";

    const items =
        Object.values(cart);


    if (items.length === 0) {

        itemsContainer.innerHTML = `
            <p>
                سبد خرید شما خالی است.
            </p>
        `;

        submitButton.disabled = true;

        return;
    }


    let total = 0;


    items.forEach(item => {

        const itemTotal =
            item.price * item.quantity;

        total += itemTotal;


        const element =
            document.createElement("div");

        element.className =
            "checkout-item";


        element.innerHTML = `
            <div>
                <strong>
                    ${item.title}
                </strong>

                <span>
                    ${item.quantity} عدد
                </span>
            </div>

            <strong>
                ${itemTotal.toLocaleString("fa-IR")}
                تومان
            </strong>
        `;


        itemsContainer.appendChild(element);

    });


    totalElement.textContent =
        `${total.toLocaleString("fa-IR")} تومان`;
}


form.addEventListener(
    "submit",
    async event => {

        event.preventDefault();


        const items =
            Object.values(cart);


        if (items.length === 0) {

            return;
        }


        const customerName =
            document.getElementById(
                "customer-name"
            ).value.trim();


        const tableNumber =
            document.getElementById(
                "table-number"
            ).value;


        const orderItems =
            items.map(item => ({

                product_id: Number(item.id),

                quantity: item.quantity

            }));


        submitButton.disabled = true;

        submitButton.textContent =
            "در حال ثبت سفارش...";


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

                            table_number:
                                Number(tableNumber),

                            items:
                                orderItems

                        })
                    }
                );


            const data =
                await response.json();


            if (!response.ok) {

                throw new Error(
                    data.detail ||
                    data.message ||
                    "ثبت سفارش ناموفق بود."
                );
            }


            localStorage.removeItem("cart");


            window.location.href =
                `/order-success/?code=${data.order_code}`;


        } catch (error) {

            messageElement.textContent =
                error.message;

            submitButton.disabled = false;

            submitButton.textContent =
                "ثبت سفارش";
        }

    }
);


renderCheckout();