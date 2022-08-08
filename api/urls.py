from django.urls import path, include
from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register('printer', views.PrinterViewSet)
router.register('cartridge', views.CartridgeViewSet)
router.register('structure', views.StructureViewSet)

urlpatterns = [
    path('cartridge/', include(router.urls)),
]
