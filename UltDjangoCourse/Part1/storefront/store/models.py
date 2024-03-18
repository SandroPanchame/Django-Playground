from django.db import models

# Create your models here.
# Framework automatically creates an ID field
class Product(models.Model):
    # sku = models.CharField(max_length=10, primary_key=True)
    # sku would be the primary key if we dont want an ID assigned by Django
    title = models.CharField(max_length=255)
    slug = models.SlugField(default='-')
    # slugs are meant to make it easier for search engines to find things (our product)
    description = models.TextField()
    unit_price = models.DecimalField(max_digits = 6, decimal_places=2)
    inventory = models.IntegerField()
    last_update = models.DateTimeField(auto_now=True)
    # look into: auto_now vs auto_now_add
    collection = models.ForeignKey('Collection', on_delete=models.PROTECT)
    # Pass in a string if a class positioning is an issue. 
    # Otherwise, move the Collection class before Product
    # A collection has many products
    promotions = models.ManyToManyField('Promotion', related_name='products')
    # M2M relation between promotions and products
    # A product can have many promotions applied to it and a promotion can apply to many products at once
    # defualt name would be product_set in promotion class. 
    # related_name = 'products' ->  would set the  attribute to 'products' in the Promotion class

class Customer(models.Model):
    MEMBERSHIP_BRONZE = 'B'
    MEMBERSHIP_SILVER = 'S'
    MEMBERSHIP_GOLD = 'G'
    MEMBERSHIP_CHOICES = [
        (MEMBERSHIP_BRONZE,'Bronze'),
        (MEMBERSHIP_SILVER, 'Silver'),
        (MEMBERSHIP_GOLD, 'Gold')
    ]
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    # unique=True -> unique value, one of
    phone = models.CharField(max_length=255)
    birth_date = models.DateField(null=True)
    # null=True -> nullable
    # Date Field -> date ; DateTimeField -> Date & Time
    membership = models.CharField(max_length=1, choices=MEMBERSHIP_CHOICES, default=MEMBERSHIP_BRONZE)
    # Choice Fields introduced here
    # # Defining Meta Data here 
    # # |
    # # V
    # class Meta:
    #     db_table='store_customers'
    #     indexes = [
    #         models.Index(fields=['first_name','last_name'])
    #     ]
    #     # indexes used speed up queries

class Order(models.Model):
    PAYMENT_PENDING = 'P'
    PAYMENT_COMPLETE = 'C'
    PAYMENT_FAILED = 'F'
    PAYMENT_STATUS = [
        (PAYMENT_PENDING, 'Pending'),
        (PAYMENT_COMPLETE, 'Complete'),
        (PAYMENT_FAILED, 'Failed'),
    ]
    placed_at = models.DateTimeField(auto_now_add=True)
    # auto_now_add=True -> automaticaly filled field
    payment_status = models.CharField(max_length=1,choices=PAYMENT_STATUS, default=PAYMENT_PENDING)
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)
    # A Customer can have many orders
    
class Address(models.Model):
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    # One to One relationship
    # customer = models.OneToOneField(Customer, on_delete=models.SET_NULL, primary_key=True)
    # SET_NULL : if the customer gets deleted the address will remain in the database but the field will be NULL
    # DEFAULT : set to a default value
    # PROTECTED : Prevent deletion of parent, delete child first, then parent
    # CASCADE : if Parent gets deleted, so does the child
    # you don't need to add an address to the customer class, django does it automatically
    # One to Many Relationship (customer may have multiple addresses)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    
class Collection(models.Model):
    title = models.CharField(max_length=255)
    featured_product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True,
        related_name='+')
    # a product can be featured multiple times? Can belong to multiple collections?
    # "fetured product of the collecton"
    # many products to a collection, they may or may not be featured
    # 0..1 featured product
    # '+' tells dango to not create reveresed relationship, we need this because the collection name is being overloaded
    # we run into an error because django is trying to create 2 reverse relationships of the same name.
    # an issue arises in a circular relationship (circular dependency)
    
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.PROTECT)
    # Order may have many order items
    product = models.ForeignKey(Product,on_delete=models.PROTECT)
    # Order may contain many products
    quantity = models.PositiveSmallIntegerField()
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)
    
class Cart(models.Model):
    created_at = models.DateTimeField(auto_now_add = True)
    # item =models.ForeignKey(Product, on_delete=models.SET_NULL)
    
class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    # cart can have many cart items
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    # products can be multiple cart items
    quantity = models.PositiveSmallIntegerField()

class Promotion(models.Model):
    description = models.CharField(max_length=255)
    discount = models.FloatField()