from django_filters.rest_framework import FilterSet
from .models import Product

class ProductFilter(FilterSet):
    class Meta:
        model = Product
        # import, filter keywords need to be in an array, even if there is 1.
        fields = {
            'collection_id': ['exact'],
            'unit_price': ['gt','lt']
        }