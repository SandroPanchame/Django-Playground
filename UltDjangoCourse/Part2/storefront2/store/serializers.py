from rest_framework import serializers
from store.models import Product, Collection
from decimal import Decimal

class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ['id','title']
    # id = serializers.IntegerField
    # title = serializers.CharField(max_length=255)
    
# serializer.Serializer -> serializer.ModelSerializer
class ProductSerializer(serializers.ModelSerializer):
    # 12 - Model Serializer
    class Meta:
        model = Product
        fields = ['id', 'title', 'unit_price', 'price_with_tax', 'collection']
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
    
    # Don't need this,  you would overide the validate method if you needed to do something extra
    # def validate(self, data):
    #     if data['password'] != data['confirm_password']:
    #         return serializers.ValidationError('Passwords do not match')
    #     return data