import openpyxl
from django.http import HttpResponse, Http404
from django.shortcuts import render, get_object_or_404


# Create your views here.
from django.utils import timezone

from stp.models import Order, BasketItem


def order_sheet_filename(order: Order):
    date_placed = str(order.date_placed.date())
    campaign_id = str(order.campaign.id)
    suffix = ".xlsx"
    return "order_" + campaign_id + "_" + date_placed + suffix


def excel_order_sheet_download(request, pk):
    wb = openpyxl.load_workbook('excel_order_sheet/exceltemplates/excel_order_sheet.xlsx')
    order = get_object_or_404(Order, pk=pk)

    if order.is_dispatched:
        raise Http404

    basket_item_set = BasketItem.objects.filter(order=order)

    for count, basket_item in enumerate(basket_item_set):
        sheet1 = wb['Sheet1']
        sheet1['B' + str(count + 2)] = order.dealer_name
        sheet1['C' + str(count + 2)] = order.recipient
        sheet1['D' + str(count + 2)] = order.zip_code
        sheet1['E' + str(count + 2)] = order.address
        sheet1['F' + str(count + 2)] = order.telephone
        sheet1['G' + str(count + 2)] = order.campaign.name
        sheet1['H' + str(count + 2)] = basket_item.item.name
        sheet1['I' + str(count + 2)] = basket_item.nos

    response = HttpResponse(content_type='application/vnd.ms-excel')

    response['Content-Disposition'] = 'attachment; filename=%s' % order_sheet_filename(order)

    wb.save(response)

    return response
