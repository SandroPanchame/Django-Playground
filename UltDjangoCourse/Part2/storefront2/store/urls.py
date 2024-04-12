from django.urls import path, include
from . import views
# with defualt router, you get two additional features. 
# they give you a root and the ability to see the data in json format
# so: <endpoint>.json
from rest_framework.routers import SimpleRouter, DefaultRouter
from rest_framework_nested import routers
# from pprint import pprint


router = routers.DefaultRouter()
router.register('products', views.ProductViewset, basename='products')
router.register('collections', views.CollectionViewSet)
router.register('carts', views.CartViewSet)
router.register('customers', views.CustomerViewSet)

carts_router = routers.NestedDefaultRouter(router,'carts', lookup='cart')
carts_router.register('items', views.CartItemViewSet, basename='cart-items')

# pprint(router.urls)
products_router = routers.NestedDefaultRouter(router,'products', lookup='product')
products_router.register('reviews', views.ReviewViewSet, basename='product-reviews')
# URLConf
# urlpatterns = router.urls
urlpatterns = router.urls + products_router.urls + carts_router.urls
# urlpatterns = [
#     path('', include(router.urls))
#     # path('products/', views.ProductList.as_view()),
#     # path('products/<int:id>/',views.ProductDetail.as_view()),
#     # path('collections/', views.CollectionList.as_view()),
#     # path('collections/<int:pk>/',views.CollectionDetail.as_view(), name='collection-detail'),
# ]