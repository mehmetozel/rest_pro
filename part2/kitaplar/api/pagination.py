from rest_framework.pagination import PageNumberPagination

class SmallPagination(PageNumberPagination):
    page_size = 5 #her istekte 5 kayit verecegiz demek
    page_query_param = 'sayfa'


class LargePagination(PageNumberPagination):
    page_size = 25