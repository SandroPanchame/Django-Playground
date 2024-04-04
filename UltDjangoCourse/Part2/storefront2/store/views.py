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
@api_view(['GET','POST'])
def product_list(request):
    if request.method == 'GET':
        query_set = Product.objects.select_related('collection').all()
        serializer = ProductSerializer(
            query_set,many=True,context={'request':request})
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = ProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        print(serializer.validated_data)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
        # if serializer.is_valid():
        #     serializer.validated_data
        #     return Response('ok')
        # else:
        #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET','PUT'])
def product_detail(request, id):
    # try:
    #     product = Product.objects.get(pk=id)
    #     serializer=ProductSerializer(product)
    #     return Response(serializer.data)
    # except Product.DoesNotExist:
    #     # statu=404 could work too
    #     return Response(status=status.HTTP_404_NOT_FOUND)
    
    # prior to the if/elif, the code would have displayed a list of products
    product = get_object_or_404(Product, pk=id)
    
    if request.method=='GET':
        
        serializer=ProductSerializer(product)
        return Response(serializer.data)
    elif request.method=='PUT':
        # passing the product object will make the serializer try and update the object with the data
        serializer = ProductSerializer(product, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

@api_view()
def collection_detail(request, pk):
    return Response('ok')