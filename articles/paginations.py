from rest_framework.pagination import CursorPagination


class CustomCursorPagination(CursorPagination):
    page_size = 5
    
    ordering = '-latest_date'
    
    cursor_query_param = 'cursor'