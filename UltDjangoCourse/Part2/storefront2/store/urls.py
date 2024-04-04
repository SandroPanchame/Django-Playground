from django.urls import path
from . import views
from rest_framework.routers import SimpleRouter
from pprint import pprint

router = SimpleRouter()
router.register('products', views.ProductViewset)
router.register('collections', views.CollectionViewSet)
pprint(router.urls)

# URLConf
urlpatterns = [
    # path('products/', views.ProductList.as_view()),
    # path('products/<int:id>/',views.ProductDetail.as_view()),
    # path('collections/', views.CollectionList.as_view()),
    # path('collections/<int:pk>/',views.CollectionDetail.as_view(), name='collection-detail'),
]