from django.shortcuts import get_object_or_404
from django.http import HttpResponse

#the rest framework has its own http REQs and RESPs. simpler and more powerful
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

# Import Serializer and model for product
from .serializers import ProductSerializer
from .models import Product

# Create your views here.
@api_view()
def product_list(request):
    query_set = Product.objects.all()
    serializer = ProductSerializer(query_set,many=True)
    return Response(serializer.data)

@api_view()
def product_detail(request, id):
    # try:
    #     product = Product.objects.get(pk=id)
    #     serializer=ProductSerializer(product)
    #     return Response(serializer.data)
    # except Product.DoesNotExist:
    #     # statu=404 could work too
    #     return Response(status=status.HTTP_404_NOT_FOUND)
    product = get_object_or_404(Product, pk=id)
    serializer=ProductSerializer(product)
    return Response(serializer.data)