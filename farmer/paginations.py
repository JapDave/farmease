from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class ProductPagination(PageNumberPagination):
      page_size = 10 
      offset = 1 
      limit = 10 
      count = 10 
      page = 1 

      def get_paginated_response(self, data):
         return Response({
            'links': {
               'next': self.get_next_link(),
               'previous': self.get_previous_link()
             },
            'total pages ': self.page.paginator.count,
            'current page': self.page.number,
            'results': data
          })

class CustomerPagination(PageNumberPagination):
      page_size = 1 
      offset = 1 
      limit = 10 
      count = 10 
      page = 1 

      def get_paginated_response(self, data):
         return Response({
            'links': {
               'next': self.get_next_link(),
               'previous': self.get_previous_link()
             },
            'total pages ': self.page.paginator.count,
            'current page': self.page.number,
            'customers': data
          })
