async function updateOrderStatus(orderCode, status) {
    try {
        const response = await fetch(
            `/api/orders/barista/update/${orderCode}/`,
            {
                method: "PATCH",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": getCookie("csrftoken"),
                },
                body: JSON.stringify({
                    status: status,
                }),
            }
        );

        const data = await response.json();

        if (!response.ok) {
            alert(data.detail || "خطا در تغییر وضعیت سفارش");
            return;
        }

        window.location.reload();

    } catch (error) {
        console.error(error);
        alert("ارتباط با سرور برقرار نشد.");
    }
}


function getCookie(name) {
    const cookies = document.cookie.split(";");

    for (const cookie of cookies) {
        const [key, value] = cookie.trim().split("=");

        if (key === name) {
            return decodeURIComponent(value);
        }
    }

    return null;
}