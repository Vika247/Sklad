"""
URL configuration for sklad project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path
from sklad import views

urlpatterns = [
    #  path('admin/', admin.site.urls),
    path('/', views.log, name="login"),  # страница автаризации
    path('user/<int:id>/', views.user, name="user"),  # страница работника
    path('admin/<int:id>/', views.admin, name="admin"),

    path('product_list/', views.product_list, name="product_list"),
    path('worker_list/', views.worker_list, name="worker_list"),
    path('order_list/', views.order_list, name="order_list"),
    path('pastav_list/', views.pastav_list, name="pastav_list"),
    path('user_list/', views.user_list, name="user_list"),
    path('zakaz_skladu/', views.zakaz_skladu, name="zakaz_skladu"),
    path('zakaz_skladu_thenk/', views.zakaz_skladu_thenk, name="zakaz_skladu_thenk"),
    path('product_list_gad/', views.roduct_list_gad, name="roduct_list_gad"),
    path('product_list_gad/product', views.product, name="product"),
    path('order_staff/<int:id>/', views.order_staff, name="order_staff"),
    path('order_list_gad/', views.order_list_gad, name="order_list_gad"),
    path('pastav_list_gad/<int:id>/', views.pastav_list_gad, name="pastav_list_gad"),
    path('user_save/', views.user_save, name="user_save"),
    path('pastav_list_gad/', views.pastav_list_gad, name="pastav_list_gad"),
    path('partner_save/', views.partner_save, name="partner_save"),
    path('zakaz_on_skladu/', views.zakaz_on_skladu, name="zakaz_on_skladu"),
    path('order_staff/<int:id>/order', views.order, name="order"),
    path('<int:id>/user_res/', views.user_res, name="user_res"),
    path('product_update/<int:id>/', views.product_update, name="product_update"),
    path('product_update/<int:id>/update_prod', views.update_prod, name="update_prod"),
    path('delete_prod/<int:id>', views.delete_prod, name="delete_prod"),
    path('delete_order/<int:id>', views.delete_order, name="delete_order"),
    path('delete_pastav/<int:id>', views.delete_pastav, name="delete_pastav"),
    path('user_delete/<int:id>', views.user_delete, name="user_delete"),
    path('pastav_update/<int:id>/', views.pastav_update, name="pastav_updatee"),
    path('pastav_update/<int:id>/update_pastav', views.update_pastav, name="update_pastav"),

    #    path('Ex', views., name='Ex'),
]
