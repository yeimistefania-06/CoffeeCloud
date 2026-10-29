from rest_framework.routers import DefaultRouter
from .views import MetodoPagoViewSet, CajaViewSet, VentaViewSet

router = DefaultRouter()
router.register('metodos-pago', MetodoPagoViewSet)
router.register('cajas', CajaViewSet)
router.register('ventas', VentaViewSet)

urlpatterns = router.urls