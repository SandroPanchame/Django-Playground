from rest_framework import serializers
from store.models import *
from decimal import Decimal
from django.db import transaction
from .signals import order_created

class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ['id','title', 'products_count']
    products_count = serializers.IntegerField(read_only=True)
    # id = serializers.IntegerField
    # title = serializers.CharField(max_length=255)
    
# serializer.Serializer -> serializer.ModelSerializer
class ProductSerializer(serializers.ModelSerializer):
    # 12 - Model Serializer
    class Meta:
        model = Product
        fields = ['id', 'title', 'description', 'slug', 'inventory', 'unit_price', 'price_with_tax', 'collection']
        # '__all__' can be used to initialize the fields variable. 
        # Bad practice, there may be things you want to keep hidden 
        # you can replace unit_price with price, just keep the line that initializes the price variable
    
    # id = serializers.IntegerField()
    # title = serializers.CharField(max_length=255)
    # price = serializers.DecimalField(max_digits=6,decimal_places=2, source='unit_price')
    price_with_tax = serializers.SerializerMethodField(method_name='calculate_tax')
    
    # 11- serializing relationships
    # collection = serializers.PrimaryKeyRelatedField(
    #     queryset=Collection.objects.all()
    # )
    # collection = serializers.StringRelatedField()
    # collection = CollectionSerializer()
    # collection = serializers.HyperlinkedRelatedField(
    #     queryset=Collection.objects.all(),
    #     view_name='collection-detail'
    # )
    
    
    def calculate_tax(self,product: Product):
        return product.unit_price * Decimal(1.1)
    
    # save method will call one of the two methods here  depedning on the state of the serializer
    # def create(self, validated_data):
    #     product = Product(**validated_data)
    #     product.other=1
    #     product.save()
    #     return product()
    #     # return super.create(validated_data)

    # def update(self,instance, validated_data):
    #     instance.unit_price = validated_data.get('unit_price')
    #     instance.save()
    #     return instance        
    
    # Don't need this,  you would overide the validate method if you needed to do something extra
    # def validate(self, data):
    #     if data['password'] != data['confirm_password']:
    #         return serializers.ValidationError('Passwords do not match')
    #     return data
    
class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id','name','description','date']
    def create(self, validated_data):
        product_id = self.context['product_id']
        return Review.objects.create(product_id = product_id, **validated_data)
    
class SimpleProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id','title', 'unit_price']
    

class CartItemSerializer(serializers.ModelSerializer):
    product = SimpleProductSerializer()
    total_price = serializers.SerializerMethodField()
    
    def get_total_price(self, cart_item: CartItem):
        return cart_item.quantity * cart_item.product.unit_price
        
    class Meta:
        model = CartItem
        fields = ['id','product','quantity', 'total_price']
    
class CartSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    items = CartItemSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField()
    
    def get_total_price(self, cart:Cart):
        return sum([item.quantity * item.product.unit_price for item in cart.items.all()])
    
    class Meta:
        model = Cart
        fields = ['id', 'items', 'total_price']
        # we can have 'items' due to related name field in CartItem model

class AddCartItemSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField()
    
    # need this to determine if a product exists
    def validate_product_id(self, value):
        if not Product.objects.filter(id=value).exists():
            raise serializers.ValidationError('no product with given id was found')
        return value
    
    def save(self, **kwargs):
        cart_id = self.context['cart_id']
        product_id = self.validated_data['product_id']
        quantity = self.validated_data['quantity']
        
        try:
            cart_item = CartItem.objects.get(cart_id = cart_id, product_id=product_id)
            cart_item.quantity += quantity
            cart_item.save()
            self.instance = cart_item
        except CartItem.DoesNotExist:
            self.instance = CartItem.objects.create(cart_id=cart_id, **self.validated_data)
            # same as adding other related data (product_id and quantity) ^
            
        return self.instance
            
    class Meta:
        model = CartItem
        fields = ['id','product_id', 'quantity']
        
class UpdateCartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['quantity']
        
class CustomerSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(read_only=True)
    class Meta:
        model = Customer
        fields = ['id','user_id','phone', 'birth_date', 'membership']
        
class OrderItemSerializer(serializers.ModelSerializer):
    product = SimpleProductSerializer
    class Meta:
        model = OrderItem
        fields = ['id','product','unit_price', 'quantity']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)
    class Meta:
        model = Order
        fields = ['id', 'customer', 'placed_at', 'payment_status', 'items']
        
class UpdateOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['payment_status']
        
class CreateOrderSerializer(serializers.BaseSerializer):
    cart_id = serializers.UUIDField()
    
    def validate_cart_id(self, cart_id):
        if not Cart.objects.filter(pk=cart_id).exists():
            raise serializers.ValidationError('No cart with the gicen ID was found.')
        if CartItem.objects.filter(cart_id=cart_id).count() == 0:
            raise serializers.ValidationError('The cart is empty')
        return cart_id
    
    def save(self, **kwargs):
        # print(self.validated_data['cart_id'])
        # print(self.context['user_id'])
        with transaction.atomic():
            customer, created = Customer.objects.get(user_id=self.context['user_id'])
            order = Order.objects.create(customer=customer)
            cart_id = self.validated_data['cart_id']
            
            cart_items = CartItem.objects \
                .select_related('product') \
                .filter(cart_id = cart_id)
                
            order_items = [
                OrderItem(
                    order = order,
                    product = item.product,
                    unit_price = item.product.unit_price,
                    quantity = item.quantity
                ) for item in cart_items
            ]
            # when an order is made, the cart is emptied
            OrderItem.objects.bulk_create(order_items)
            Cart.objects.filter(pk=cart_id).delete()

            order_created.send_robust(self.__class__ , order=order)
            
            return order    
        