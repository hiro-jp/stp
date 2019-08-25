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
from django.contrib.staticfiles.urls import static, staticfiles_urlpatterns
from django.urls import path, include

from stp import settings
from stp.views import CampaignListView, campaign_detail_view, order_create_view, OrderApproveListView, order_approve_view, \
    order_dispatch_view, OrderDetailView, OrderListView, OrderDispatchListView, IndexView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),

    path('', IndexView.as_view(), name="index"),

    path('campaign/', CampaignListView.as_view(), name='campaign_list'),
    path('campaign/<int:pk>', campaign_detail_view, name="campaign_detail"),

    path('order/approve/', OrderApproveListView.as_view(), name="order_approve_list"),
    path('order/approve/<int:pk>', order_approve_view, name="order_approve_detail"),

    path('order/dispatch/', OrderDispatchListView.as_view(), name="order_dispatch_list"),
    path('order/dispatch/<int:pk>', order_dispatch_view, name="order_dispatch_detail"),

    path('order/', OrderListView.as_view(), name="order_list"),
    path('order/<int:pk>', OrderDetailView.as_view(), name="order_detail"),
    path('order/create/<int:pk>', order_create_view, name="order_create"),

    path('excel_order_sheet/', include('excel_order_sheet.urls')),
]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
