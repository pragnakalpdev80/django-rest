from rest_framework.pagination import LimitOffsetPagination, PageNumberPagination 

class BookLimitOffsetPagination(LimitOffsetPagination):

    default_limit = 20
    limit_query_param = 'limit'
    offset_query_param = 'offset'
    max_limit = 100


class CustomPageNumberPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100
    
    def get_paginated_response(self, data):
        response = super().get_paginated_response(data)
        # Add custom metadata
        response.data['custom_field'] = 'custom_value'
        return response