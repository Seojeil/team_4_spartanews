from rest_framework.pagination import CursorPagination


class CustomCursorPagination(CursorPagination):
    page_size = 5
    
    cursor_query_param = 'cursor'
    
    ordering ='-latest_date'
    
    def get_ordering(self, request, queryset, view):
        sort_type = request.query_params.get("sort_type", "")
        if sort_type == 'recommendation':
            return ('-recommendation_count', '-latest_date')
        elif sort_type == 'hits':
            return ("-hits", "-latest_date")
        return ('-latest_date',)