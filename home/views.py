from django.shortcuts import render
from django.http.request import HttpRequest
from django.views import View
from .models import Product
from .tasks import all_bucket_objects_tasks

# Create your views here.


class HomeView(View):
    template_name = "home/home.html"

    def get(self, request: HttpRequest):
        products = Product.objects.filter(available=True)
        return render(request, self.template_name, {"products": products})


class ProductDetailView(View):
    template_name = "home/detail.html"

    def get(self, request, *args, **kwargs):
        product_id, product_slug = kwargs["product_id"], kwargs["product_slug"]
        product = Product.objects.get(pk=product_id, slug=product_slug)
        return render(request, self.template_name, {"product": product})


class BucketHomeView(View):
    template_name = "home/bucket.html"

    def get(self, request, *args, **kwargs):
        objects = all_bucket_objects_tasks()
        return render(request, self.template_name, {"objects": objects})
