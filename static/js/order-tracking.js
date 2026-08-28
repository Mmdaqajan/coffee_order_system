const form =
    document.getElementById(
        "tracking-form"
    );


const input =
    document.getElementById(
        "order-code"
    );


const result =
    document.getElementById(
        "tracking-result"
    );


form.addEventListener(
    "submit",
    async event => {

        event.preventDefault();


        const orderCode =
            input.value.trim();


        if (!orderCode) {
            return;
        }


        result.innerHTML = `
            <p>
                در حال دریافت اطلاعات...
            </p>
        `;


        try {

            const response =
                await fetch(
                    `/api/orders/status/${encodeURIComponent(orderCode)}/`
                );


            const data =
                await response.json();


            if (!response.ok) {

                throw new Error(
                    data.detail ||
                    "سفارش پیدا نشد."
                );
            }


            result.innerHTML = `

                <div class="order-status-card">

                    <h2>
                        سفارش #${data.order_code}
                    </h2>


                    <p>
                        مشتری:
                        ${data.customer_name}
                    </p>


                    <p>
                        وضعیت:
                        <strong>
                            ${data.status_display}
                        </strong>
                    </p>


                    <p>
                        مبلغ:
                        ${Number(
                            data.total_price
                        ).toLocaleString("fa-IR")}

                        تومان
                    </p>


                    <h3>
                        محصولات
                    </h3>


                    <div>

                        ${data.items.map(
                            item => `

                                <div>

                                    ${item.product_title}

                                    ×

                                    ${item.quantity}

                                    -

                                    ${Number(
                                        item.price
                                    ).toLocaleString("fa-IR")}

                                    تومان

                                </div>

                            `
                        ).join("")}

                    </div>

                </div>

            `;

        } catch (error) {

            result.innerHTML = `

                <p>
                    ${error.message}
                </p>

            `;

        }

    }
);