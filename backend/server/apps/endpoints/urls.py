from django.conf.urls import url
from django.conf.urls import include
from rest_framework.routers import DefaultRouter

from apps.endpoints.views import EndpointViewset
from apps.endpoints.views import MLAlgorithmViewset
from apps.endpoints.views import MLRequestViewset
from apps.endpoints.views import PredictView

router = DefaultRouter(trailing_slash=False)
router.register(r"endpoints", EndpointViewset, basename='endpoints')
router.register(r"mlalgorithms", MLAlgorithmViewset, basename='mlalgorithms')
router.register(r"mlrequests", MLRequestViewset, basename='mlrequests')

urlpatterns = [
    url(r"^api/v1/", include(router.urls)),
    # add predict url
    url(
        r"^api/v1/(?P<endpoint_name>.+)/predict$", PredictView.as_view(), name="predict"
    ),
]
