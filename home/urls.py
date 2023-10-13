from django.urls import path
from .views import *

app_name = "home"

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path(
        "product-detail/<int:product_id>/<slug:product_slug>",
        ProductDetailView.as_view(),
        name="product-detail",
    ),
]
