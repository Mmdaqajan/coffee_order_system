from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render


@login_required(login_url="/barista/login/")
def barista_dashboard(request):
    """
    نمایش پنل باریستا فقط برای کاربران دارای Role باریستا.
    """

    # اگر کاربر Profile نداشته باشد، اجازه ورود ندارد.
    if not hasattr(request.user, "profile"):
        return redirect("barista-login")

    # فقط کاربران دارای Role باریستا وارد پنل می‌شوند.
    if request.user.profile.role != "barista":
        return redirect("/")

    # فقط سفارش‌های فعال برای باریستا نمایش داده می‌شوند.
    orders = (
        Order.objects
        .exclude(
            status__in=["completed", "canceled"]
        )
        .prefetch_related("items__product")
    )

    return render(
        request,
        "dashboard.html",
        {
            "orders": orders,
        },
    )