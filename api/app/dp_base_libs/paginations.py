from rest_framework.pagination import PageNumberPagination
from dp_base_libs.rewrites.base_paginator import DPBasePaginator


class DPAngularTablePagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'limit'
    max_page_size = 1000
    django_paginator_class = DPBasePaginator

    def get_page_size(self, request):
        if self.page_size_query_param:
            try:
                if request.query_params[self.page_size_query_param] == '0':
                    return None
                else:
                    return super(DPAngularTablePagination, self).get_page_size(request)
            except (KeyError, ValueError):
                pass

        return self.page_size