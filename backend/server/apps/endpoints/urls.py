from django.conf.urls import url
from django.conf.urls import include
from rest_framework.routers import DefaultRouter

from apps.endpoints.views import EndpointViewset
from apps.endpoints.views import MLAlgorithmViewset
from apps.endpoints.views import MLAlgorithmStatusViewset
from apps.endpoints.views import MLRequestViewset
from apps.endpoints.views import PredictView
from apps.endpoints.views import ABTestViewSet
from apps.endpoints.views import StopABTestView

router = DefaultRouter(trailing_slash=False)
router.register(r"endpoints", EndpointViewset, basename='endpoints')
router.register(r"mlalgorithms", MLAlgorithmViewset, basename='mlalgorithms')
router.register(r"mlalgorithmstatuses", MLAlgorithmStatusViewset,
                basename="mlalgorithmstatuses")
router.register(r"mlrequests", MLRequestViewset, basename='mlrequests')
router.register(r"abtests", ABTestViewSet, basename='abtests')

urlpatterns = [
    url(r"^api/v1/", include(router.urls)),
    # add predict url
    url(
        r"^api/v1/(?P<endpoint_name>.+)/predict$", PredictView.as_view(), name="predict"
    ),
    url(
        r"^api/v1/stop_ab_test/(?P<ab_test_id>.+)", StopABTestView.as_view(), name="stop_ab"
    ),
]
