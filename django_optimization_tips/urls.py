"""django_optimization_tips URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from products.views import ProductsView, ProductTableView, \
    ProductTableCallbackView

urlpatterns = [
    path(r"", ProductsView.as_view(), name="products"),
    path(r"table/", ProductTableView.as_view(), name="products_table"),
    path(
        r"table_callback/",
        ProductTableCallbackView.as_view(),
        name="table_callback"
    ),

    path('admin/', admin.site.urls),
]
