message = "شما دسترسی باریستا را ندارید."

def has_permission(self, request, view):
    # بررسی می‌کنیم کاربر وارد حساب شده باشد.
    if not request.user or not request.user.is_authenticated:
        return False

    # بررسی می‌کنیم کاربر Profile داشته باشد.
    if not hasattr(request.user, "profile"):
        return False

    # فقط Role باریستا اجازه دسترسی دارد.
    return request.user.profile.role == "barista"