from rest_framework.pagination import PageNumberPagination


class DPAngularTablePagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'limit'
    max_page_size = 1000

    def get_page_size(self, request):
        if self.page_size_query_param:
            try:
                if request.query_params[self.page_size_query_param] == '0':
                    return None
            except (KeyError, ValueError):
                pass

        return self.page_size