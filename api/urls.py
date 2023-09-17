from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import CurrencyConversionViewSet, CurrencyListViewSet

app_name = 'api'

router = DefaultRouter()
router.register(r'currencies', CurrencyListViewSet, basename='currencies')
router.register(r'rates', CurrencyConversionViewSet, basename='currency_converter')

urlpatterns = [
    path('api/', include(router.urls)),
]
