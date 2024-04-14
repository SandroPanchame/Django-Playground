from django.shortcuts import get_object_or_404
# from django.http import HttpResponse

from django_filters.rest_framework import DjangoFilterBackend

#the rest framework has its own http REQs and RESPs. simpler and more powerful
from rest_framework.decorators import api_view
# from rest_framework.views import APIView
# from rest_framework.mixins import ListModelMixin, CreateModelMixin
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, DestroyModelMixin, UpdateModelMixin
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser, DjangoModelPermissions,DjangoModelPermissionsOrAnonReadOnly

# Import Serializer and model for product
from .serializers import *
from .models import Product, Collection, OrderItem, Review
from .pagination import DefaultPagination
from .filters import ProductFilter
from .permissions import IsAdminOrReadOnly, FullDjangoModelPermissions, ViewCustomerHistoryPermission

from django.db.models import Count

class ProductViewset(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = ProductFilter
    pagination_class = DefaultPagination
    permission_classes = [IsAdminOrReadOnly]
    search_fields = ['title', 'description']    
    ordering_fields = ['unit_price', 'last_update']
    # filterset_fields = ['collection_id', 'unit_price']
    # the following line is why we cant use pk. product_id, product_pk
    lookup_field='id' 
    # if the filtering backend was unavailable, use the code below
    # def get_queryset(self):
    #     queryset = Product.objects.all()
    #     collection_id = self.request.query_params.get('collection_id')
    #     if collection_id is not None:
    #         queryset = queryset.filter(collection_id=collection_id)
    #     return queryset
    
    def get_serializer_context(self):
        return {'request': self.request}
    
    def destroy(self, request, *args, **kwargs):
        if OrderItem.objects.filter(product_id= kwargs['pk']).count() > 0:
            return Response(
                {"error": 'product cannot be deleted due to association'},
                status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().destroy(request, *args, **kwargs)
    
    # def delete(self, request, id):
    #     product = get_object_or_404(Product, pk=id)
    #     if product.orderitems.count() > 0:
    #         return Response(
    #             {"error": 'product cannot be deleted due to association'},
    #             status=status.HTTP_405_METHOD_NOT_ALLOWED)
    #     product.delete()
    #     return Response(status=status.HTTP_204_NO_CONTENT)
    
class CollectionViewSet(ModelViewSet):
    queryset = Collection.objects.annotate(
        products_count=Count('products')).all()
    serializer_class = CollectionSerializer
    permission_classes = [IsAdminOrReadOnly]
    
    def destroy(self, request, *args, **kwargs):
        if Product.objects.filter(collection_id=kwargs['pk']).count() > 0:
            # print(Product.objects.filter(collection_id=kwargs['pk']).count()) [252, id = 3]
        # collection.products.count() > 0:
            return Response({'error':'Collection cannot be deleted because it includes one or more products'}, 
                            status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().destroy(request, *args, **kwargs)
    
    # def delete(self,request,pk):
    #     collection =get_object_or_404(Collection, pk=pk)
    #     if collection.products.count() > 0:
    #         return Response({'error':'Collection cannot be deleted because it includes one or more products'}, 
    #                         status=status.HTTP_405_METHOD_NOT_ALLOWED)
    #     collection.delete()
    #     return Response(status=status.HTTP_204_NO_CONTENT)
class ReviewViewSet(ModelViewSet):
    # queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    
    def get_queryset(self):
        return Review.objects.filter(product_id = self.kwargs['product_id'])
    
    def get_serializer_context(self):
        return {'product_id': self.kwargs['product_id']}
        # used the product_pk keyword, didn't work.
        # probably due to a change i made
# the inheritance here prevents GET  of all carts
# List Model Mixin is responsible for it
class CartViewSet(CreateModelMixin,
                  RetrieveModelMixin,
                  DestroyModelMixin,
                  GenericViewSet):
    # Use prefetch for many items, use select_related for singular
    queryset = Cart.objects.prefetch_related('items__product').all()
    serializer_class = CartSerializer
    
    # def get_queryset(self):
    #     return Cart.objects.filter(cart_id = self.kwargs['cart_id'])
    
    # def get_serializer_context(self):
    #     return {'request': self.request}
    
    
    
class CartItemViewSet(ModelViewSet):

    # serializer_class = CartItemSerializer
    # Method names in the array must be lower case
    http_method_names = ['get','post','patch','delete']
    def get_serializer_class(self):
        
        if self.request.method=='POST':
            return AddCartItemSerializer
        elif self.request.method=='PATCH':
            return UpdateCartItemSerializer
        return CartItemSerializer
    
    def get_serializer_context(self):
        return {'cart_id': self.kwargs['cart_pk']}
    
    def get_queryset(self):
        return CartItem.objects \
            .filter(cart_id = self.kwargs['cart_pk']) \
            .select_related('product')
# permission classes can be used as a substitute for Model Mixins?
class CustomerViewSet(ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    # With Django Model Permissions, user has to be authenticated and 
    # have the relevant model permissions
    # sometime IsAdminUser is good enough
    permission_classes = [IsAdminUser]
    
    # for permissions, allowed to recieve, but not update
    def  get_permissions(self):
        if self.request.method =='GET':
            return [AllowAny()]
        return[IsAuthenticated()]
    
    # methods referred to as actions
    # detail = False : available on list view
    # if True, available on the detail view
    @action(detail=False, methods=['GET','PUT'], permission_classes=[IsAuthenticated])
    def me(self, request):
        customer, created = Customer.objects.get_or_create(user_id=request.user.id)
        if request.method == 'GET':
            customer = Customer.objects.get(user_id=request.user.id)
            serializer = CustomerSerializer(customer)
            return Response(serializer.data)
        elif request.method == 'PUT':
            serializer = CustomerSerializer(customer, data = request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
    
    @action(detail=True, permission_classes=[ViewCustomerHistoryPermission])        
    def history(self, request, pk):
        return Response('ok')
            
class OrderViewSet(ModelViewSet):
    #  queryset = Order.objects.all()
    # serializer_class = OrderSerializer
    # permission_classes = [IsAuthenticated]
    # you can use get_permissions instead of setting up the classes
    http_method_names = ['get','patch','delete','head', 'options']
    
    def get_permissions(self):
        if self.request.method in ['PATCH','DELETE']:
            return [IsAdminUser()]
        return[IsAuthenticated()]
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CreateOrderSerializer
        return OrderSerializer
    
    # method commented out, no longer need to rely on a mixin
    # def get_serializer_context(self):
    #     return {'user_id':self.request.user.id}
     
    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Order.objects.all()
        customer_id, created = Customer.objects.get_or_create(user_id = user.id)
        return Order.objects.filter(customer_id=customer_id)  
    
    def create(self, request, *args, **kwargs):
        serializer = CreateOrderSerializer(
            data=request.data,
            context= {'user_id':self.request.user.id})
        serializer.is_valid(raise_exception=True)
        order = serializer.save()
        serializer = OrderSerializer(order)
        return Response(serializer.data)
    
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
