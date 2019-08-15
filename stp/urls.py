"""stp URL Configuration

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

from stp.views import IndexView, detail_view, edit_view, order_create_view, OrderApproveListView, order_approve_view, \
    order_dispatch_view, MyOrderDetailView, MyOrderListView, OrderDispatchListView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', IndexView.as_view(), name='index'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('detail/<int:pk>', detail_view, name="detail"),
    path('edit/', edit_view, name="edit"),
    path('order/create/<int:pk>', order_create_view, name="order"),
    path('approve/list/', OrderApproveListView.as_view(), name="approve_list"),
    path('approve/<int:pk>', order_approve_view, name="approve"),
    path('dispatch/<int:pk>', order_dispatch_view, name="dispatch"),
    path('dispatch/list/', OrderDispatchListView.as_view(), name="dispatch_list"),
    path('order/detail/<int:pk>', MyOrderDetailView.as_view(), name="order_detail"),
    path('order/detail/list/', MyOrderListView.as_view(), name="order_list"),
]
