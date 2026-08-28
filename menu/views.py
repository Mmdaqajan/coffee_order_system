from django.views.generic import TemplateView


class HomeView(TemplateView):
    template_name = "index.html"


class CartView(TemplateView):
    template_name = "cart.html"


class CheckoutView(TemplateView):
    template_name = "checkout.html"


class OrderSuccessView(TemplateView):
    template_name = "order_success.html"


class OrderTrackingView(TemplateView):
    template_name = "order_tracking.html"