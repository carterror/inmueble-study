from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination


class InmueblePagination(LimitOffsetPagination):
    default_limit = 1
    max_limit = 10
    limit_query_param = 'limit'
    offset_query_param = 'offset'
    ordering = 'id'
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

