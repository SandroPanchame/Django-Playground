from django.shortcuts import get_object_or_404
from django.http import HttpResponse

#the rest framework has its own http REQs and RESPs. simpler and more powerful
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.mixins import ListModelMixin, CreateModelMixin
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework import status

# Import Serializer and model for product
from .serializers import ProductSerializer, CollectionSerializer
from .models import Product, Collection

from django.db.models import Count

class ProductViewset(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class=ProductSerializer
    lookup_field='id'
    def get_serializer_context(self):
        return {'request': self.request}
    
    def delete(self, request, id):
        product = get_object_or_404(Product, pk=id)
        if product.orderitems.count() > 0:
            return Response(
                {"error": 'product cannot be deleted due to association'},
                status=status.HTTP_405_METHOD_NOT_ALLOWED)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class CollectionViewSet(ModelViewSet):
    queryset = Collection.objects.annotate(
        products_count=Count('products')).all()
    serializer_class = CollectionSerializer
    def delete(self,request,pk):
        collection =get_object_or_404(Collection, pk=pk)
        if collection.products.count() > 0:
            return Response({'error':'Collection cannot be deleted because it includes one or more products'}, 
                            status=status.HTTP_405_METHOD_NOT_ALLOWED)
        collection.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
     

# # class based view, cleaner code
# class ProductList(ListCreateAPIView):
#     # queryset = Product.objects.all()
#     # serializer_class=ProductSerializer
#     # overrides the function from ListCreateAPIView
#     # if you want to apply some logic, apply them in these function definitions
#     # otherwise, go with the above
#     # def get_queryset(self):
#     #     return Product.objects.select_related('collection').all()
    
#     # def get_serializer_class(self):
#     #     return ProductSerializer
    
#     # def get_serializer_context(self):
#     #     return {'request': self.request}
     
#     # def get(self,request):
#     #     query_set = Product.objects.select_related('collection').all()
#     #     serializer = ProductSerializer(
#     #         query_set,many=True,context={'request':request})
#     #     return Response(serializer.data)
    
#     # def post(self, request):
#     #     serializer = ProductSerializer(data=request.data)
#     #     serializer.is_valid(raise_exception=True)
#     #     serializer.save()
#     #     # print(serializer.validated_data)
#     #     return Response(serializer.data, status=status.HTTP_201_CREATED)
    
# class ProductDetail(RetrieveUpdateDestroyAPIView):
#     queryset = Product.objects.all()
#     serializer_class=ProductSerializer
#     # generally, would need pk. can overide with 'lookup_field'
#     lookup_field='id'
#     # def get(self, request, id):
#     #     product = get_object_or_404(Product, pk=id)
#     #     serializer = ProductSerializer(product)
#     #     return Response(serializer.data)
#     # def put(self, request, id):
#     #     product = get_object_or_404(Product, pk=id)
#     #     serializer = ProductSerializer(product, data=request.data)
#     #     serializer.is_valid(raise_exception=True)
#     #     serializer.save()
#     #     return Response(serializer.data)
#     def delete(self, request, id):
#         product = get_object_or_404(Product, pk=id)
#         if product.orderitems.count() > 0:
#             return Response(
#                 {"error": 'product cannot be deleted due to association'},
#                 status=status.HTTP_405_METHOD_NOT_ALLOWED)
#         product.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
    
class CollectionList(ListCreateAPIView):
    queryset = Collection.objects.annotate(
        products_count=Count('products')).all()
    serializer_class = CollectionSerializer

class CollectionDetail(RetrieveUpdateDestroyAPIView):
    queryset = Collection.objects.annotate(
        products_count=Count('products'))
    serializer_class = CollectionSerializer
    
    def delete(self,request,pk):
        collection =get_object_or_404(Collection, pk=pk)
        if collection.products.count() > 0:
            return Response({'error':'Collection cannot be deleted because it includes one or more products'}, 
                            status=status.HTTP_405_METHOD_NOT_ALLOWED)
        collection.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
        
    
# # Create your views here.
# @api_view(['GET','POST'])
# def product_list(request):
#     if request.method == 'GET':
#         query_set = Product.objects.select_related('collection').all()
#         serializer = ProductSerializer(
#             query_set,many=True,context={'request':request})
#         return Response(serializer.data)
#     elif request.method == 'POST':
#         serializer = ProductSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         print(serializer.validated_data)
#         return Response(serializer.data, status=status.HTTP_201_CREATED)
#         # if serializer.is_valid():
#         #     serializer.validated_data
#         #     return Response('ok')
#         # else:
#         #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET','PUT', 'DELETE'])
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
        serializer = ProductSerializer(product)
        return Response(serializer.data)
    elif request.method=='PUT':
        # passing the product object will make the serializer try and update the object with the data
        serializer = ProductSerializer(product, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    elif request.method == 'DELETE':
        if product.orderitems.count() > 0:
            return Response(
                {"error": 'product cannot be deleted due to association'},status=status.HTTP_405_METHOD_NOT_ALLOWED)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET','PUT','DELETE'])
def collection_detail(request, pk):
    collection =get_object_or_404(
        Collection.objects.annotate(
            products_count=Count('products')), pk=pk
        )
    if request.method == 'GET':
        serializer = CollectionSerializer(collection)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = CollectionSerializer(collection, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    elif request.method == 'DELETE':
        if collection.products.count() > 0:
            return Response({'error':'Collection cannot be deleted because it includes one or more products'}, 
                            status=status.HTTP_405_METHOD_NOT_ALLOWED)
        collection.delete
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET','POST'])
def collection_list(request):
    if request.method == 'GET':
        queryset = Collection.objects.annotate(products_count=Count('products')).all()
        serializer = CollectionSerializer(queryset, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = CollectionSerializer(data = request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response('ok')
