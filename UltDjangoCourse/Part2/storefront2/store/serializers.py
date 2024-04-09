from rest_framework import serializers
from store.models import *
from decimal import Decimal

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
    pass

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
        return sum([item.quantity * item.product.unit_price for item in cart.item.all()])
    
    class Meta:
        model = Cart
        fields = ['id', 'items', 'total_price']
        # we can have 'items' due to related name field in CartItem model

