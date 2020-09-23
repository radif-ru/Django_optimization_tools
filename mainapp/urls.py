"""shop URL Configuration

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
from django.urls import path

import mainapp.views as mainapp

app_name = 'mainapp'

urlpatterns = [
    path('', mainapp.index, name='index'),
    path('products/', mainapp.products, name='products'),

    path('category/<int:pk>/catalog/', mainapp.catalog, name='catalog'),
    # re_path(r'^category/(?P<pk>\d+)/catalog/$', mainapp.catalog, name='catalog'),
    path('category/<int:pk>/catalog/<int:page>/', mainapp.catalog, name='catalog_page'),

    path('showroom/', mainapp.showroom, name='showroom'),
    path('category/<int:pk>/showroom/', mainapp.showroom, name='showroom_catalog'),
    path('category/<int:pk>/showroom/<int:page>/', mainapp.showroom, name='showroom_catalog_page'),

    path('product/<int:pk>/', mainapp.product_page, name='product_page'),

    path('contact/', mainapp.contact, name='contact'),
]
