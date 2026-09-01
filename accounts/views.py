from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render


def barista_login(request):
    if request.user.is_authenticated:
        if hasattr(request.user, "profile") and request.user.profile.role == "barista":
            return redirect("barista-dashboard")

        return redirect("/")

    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "")

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

        if not user.is_active:
            return render(
                request,
                "accounts/barista_login.html",
                {
                    "error": "حساب کاربری شما غیرفعال است.",
                },
            )

        if not hasattr(user, "profile") or user.profile.role != "barista":
            return render(
                request,
                "accounts/barista_login.html",
                {
                    "error": "این حساب، حساب باریستا نیست.",
                },
            )

        login(request, user)

        return redirect("barista-dashboard")

    return render(
        request,
        "accounts/barista_login.html",
    )


@login_required(login_url="/barista/login/")
def barista_logout(request):
    logout(request)
    return redirect("barista-login")