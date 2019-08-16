from django.urls import path
from . import views

app_name = 'excel_order_sheet'
urlpatterns = [
    path('<int:pk>', views.excel_order_sheet_download, name='excel_order_sheet')
]
