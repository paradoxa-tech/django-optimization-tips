import logging

from django.http import JsonResponse, HttpResponseBadRequest
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_protect
from django.views.generic import TemplateView

from products.helpers import ProcessTableData

logger = logging.getLogger('django')


class ProductsView (TemplateView):
    template_name = 'products.html'


class ProductTableView(View):
    @method_decorator(csrf_protect)
    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            raw_data = self.request.POST
            page_length = int(raw_data['length'])
            start = int(raw_data['start'])
            order_column = raw_data['order[0][column]']
            order_dir = raw_data['order[0][dir]']
            search = raw_data['search[value]']

            process_table_data = ProcessTableData(
                page_length, start, order_column, order_dir, search
            )
            total_records = process_table_data.calculate_total_records()
            process_table_data.sort_data()
            process_table_data.search_data()
            data = process_table_data.get_data()
            filtered_records = len(data)
            data = data[start:start + page_length]

            table_data = {
                'recordsTotal': total_records,
                'recordsFiltered': filtered_records,
                'data': data,
                'draw': raw_data['draw']
            }

            return JsonResponse(
                status=200, data=table_data, content_type="application/json"
            )
        return HttpResponseBadRequest()
