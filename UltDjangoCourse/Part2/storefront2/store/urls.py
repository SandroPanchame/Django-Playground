from django.urls import path, include
from . import views
# with defualt router, you get two additional features. 
# they give you a root and the ability to see the data in json format
# so: <endpoint>.json
from rest_framework.routers import SimpleRouter, DefaultRouter
# from pprint import pprint


router = DefaultRouter()
router.register('products', views.ProductViewset)
router.register('collections', views.CollectionViewSet)
# pprint(router.urls)

# URLConf
# urlpatterns = router.urls
urlpatterns = [
    path('', include(router.urls))
    # path('products/', views.ProductList.as_view()),
    # path('products/<int:id>/',views.ProductDetail.as_view()),
    # path('collections/', views.CollectionList.as_view()),
    # path('collections/<int:pk>/',views.CollectionDetail.as_view(), name='collection-detail'),
]