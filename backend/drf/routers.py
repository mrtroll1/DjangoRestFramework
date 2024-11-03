# Usually include routers in urls

from rest_framework.routers import DefaultRouter

from products.viewsets import ProductViewSet

router = DefaultRouter()
router.register('products', ProductViewSet, basename='products') # routers don't give granual control (they are made exactly for you not to do it)

urlpatterns = router.urls