from rest_framework.routers import DefaultRouter
from .views import (
    ClienteViewSet, CreditoViewSet, AbonoViewSet,
    ComprobantePagoViewSet, AcuerdoPagoViewSet, EstadoCuentaViewSet,
)

router = DefaultRouter()
router.register('clientes', ClienteViewSet)
router.register('creditos', CreditoViewSet)
router.register('abonos', AbonoViewSet)
router.register('comprobantes', ComprobantePagoViewSet)
router.register('acuerdos-pago', AcuerdoPagoViewSet)
router.register('estados-cuenta', EstadoCuentaViewSet)

urlpatterns = router.urls