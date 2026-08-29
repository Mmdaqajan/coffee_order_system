import requests
from django.conf import settings


# =========================================================
# تنظیمات زرین‌پال
# =========================================================

ZARINPAL_REQUEST_URL = (
    "https://api.zarinpal.com/pg/v4/payment/request.json"
)

ZARINPAL_VERIFY_URL = (
    "https://api.zarinpal.com/pg/v4/payment/verify.json"
)

ZARINPAL_STARTPAY_URL = (
    "https://www.zarinpal.com/pg/StartPay/"
)


# =========================================================
# ایجاد درخواست پرداخت
# =========================================================

def create_payment_request(
    amount,
    description,
    callback_url,
):
    """
    ارسال درخواست ایجاد تراکنش به زرین‌پال.

    amount:
        مبلغ پرداخت به ریال

    description:
        توضیحات تراکنش

    callback_url:
        آدرسی که بعد از پرداخت،
        زرین‌پال کاربر را به آن برمی‌گرداند.
    """

    data = {
        "merchant_id": settings.ZARINPAL_MERCHANT_ID,
        "amount": int(amount),
        "description": description,
        "callback_url": callback_url,
    }

    try:

        response = requests.post(
            ZARINPAL_REQUEST_URL,
            json=data,
            headers={
                "Content-Type": "application/json",
            },
            timeout=15,
        )

        response.raise_for_status()

        result = response.json()

    except requests.RequestException as error:

        raise Exception(
            f"خطا در ارتباط با زرین‌پال: {error}"
        )


    # -----------------------------------------------------
    # بررسی پاسخ زرین‌پال
    # -----------------------------------------------------

    data = result.get("data", {})

    code = data.get("code")


    if code != 100:

        errors = result.get("errors", {})

        raise Exception(
            f"خطا در ایجاد پرداخت زرین‌پال: "
            f"{errors or data}"
        )


    authority = data.get("authority")


    if not authority:

        raise Exception(
            "زرین‌پال Authority معتبری برنگرداند."
        )


    # -----------------------------------------------------
    # ساخت لینک انتقال کاربر به درگاه
    # -----------------------------------------------------

    payment_url = (
        f"{ZARINPAL_STARTPAY_URL}"
        f"{authority}"
    )


    return {
        "authority": authority,
        "payment_url": payment_url,
    }


# =========================================================
# تأیید پرداخت
# =========================================================

def verify_payment(
    authority,
    amount,
):
    """
    تأیید تراکنش توسط زرین‌پال.

    این تابع فقط زمانی باید اجرا شود که
    Callback با Status=OK برگشته باشد.
    """

    data = {
        "merchant_id": settings.ZARINPAL_MERCHANT_ID,
        "amount": int(amount),
        "authority": authority,
    }


    try:

        response = requests.post(
            ZARINPAL_VERIFY_URL,
            json=data,
            headers={
                "Content-Type": "application/json",
            },
            timeout=15,
        )

        response.raise_for_status()

        result = response.json()

    except requests.RequestException as error:

        raise Exception(
            f"خطا در ارتباط با زرین‌پال: {error}"
        )


    # -----------------------------------------------------
    # اطلاعات پاسخ زرین‌پال
    # -----------------------------------------------------

    data = result.get("data", {})

    code = data.get("code")

    ref_id = data.get("ref_id")


    # -----------------------------------------------------
    # کد 100 = پرداخت با موفقیت تأیید شد
    # کد 101 = تراکنش قبلاً تأیید شده
    # -----------------------------------------------------

    if code in [100, 101]:

        return {
            "success": True,
            "code": code,
            "ref_id": ref_id,
            "data": data,
        }


    # -----------------------------------------------------
    # پرداخت تأیید نشد
    # -----------------------------------------------------

    errors = result.get("errors", {})

    return {
        "success": False,
        "code": code,
        "ref_id": ref_id,
        "errors": errors,
        "data": data,
    }

