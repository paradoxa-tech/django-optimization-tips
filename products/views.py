import time

from django.db import connection
from django.http import JsonResponse, HttpResponseBadRequest
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_protect
from django.views.generic import TemplateView

from products.helpers import ProcessTableData
from products.models import Measurement


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

            initial_number_of_queries = len(connection.queries)
            initial_time = time.time()
            process_table_data = ProcessTableData(
                page_length, start, order_column, order_dir, search
            )
            total_records = process_table_data.calculate_total_records()
            process_table_data.sort_data()
            process_table_data.search_data()
            data = process_table_data.get_data()
            filtered_records = len(data)
            data = data[start:start + page_length]

            number_of_queries = \
                len(connection.queries) - initial_number_of_queries
            request_time = time.time() - initial_time
            Measurement.objects.create(
                request_time=request_time,
                number_of_queries=number_of_queries
            )
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


class ProductTableCallbackView(View):

    @method_decorator(csrf_protect)
    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            measurement = \
                Measurement.objects.all().order_by("-created_at").first()
            data = {
                "queries": measurement.number_of_queries,
                "time": measurement.request_time
            }
            return JsonResponse(
                status=200, data=data, content_type="application/json"
            )
        return HttpResponseBadRequest()
