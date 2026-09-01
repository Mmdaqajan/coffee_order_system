from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render


def barista_login(request):
    """
    ورود باریستا با نام کاربری و رمز عبور Django.
    """

    # اگر کاربر از قبل وارد شده باشد، مستقیماً به پنل باریستا می‌رود.
    if request.user.is_authenticated:
        if hasattr(request.user, "profile") and request.user.profile.role == "barista":
            return redirect("barista-dashboard")

        return redirect("/")

    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "")

        # بررسی نام کاربری و رمز عبور توسط سیستم احراز هویت Django.
        user = authenticate(
            request,
            username=username,
            password=password,
        )

        if user is None:
            return render(
                request,
                "accounts/barista_login.html",
                {
                    "error": "نام کاربری یا رمز عبور اشتباه است.",
                },
            )

        # فقط حساب‌هایی که Role آنها barista است اجازه ورود دارند.
        if not hasattr(user, "profile") or user.profile.role != "barista":
            return render(
                request,
                "accounts/barista_login.html",
                {
                    "error": "این حساب، حساب باریستا نیست.",
                },
            )

        # حساب غیرفعال اجازه ورود ندارد.
        if not user.is_active:
            return render(
                request,
                "accounts/barista_login.html",
                {
                    "error": "حساب کاربری شما غیرفعال است.",
                },
            )

        # ساخت Session برای کاربر.
        login(request, user)

        return redirect("barista-dashboard")

    return render(
        request,
        "accounts/barista_login.html",
    )


@login_required(login_url="/barista/login/")
def barista_logout(request):
    """
    خروج باریستا از Session.
    """

    logout(request)

    return redirect("barista-login")