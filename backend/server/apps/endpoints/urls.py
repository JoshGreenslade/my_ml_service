from django.conf.urls import url
from django.conf.urls import include
from rest_framework.routers import DefaultRouter

from apps.endpoints.views import EndpointViewset
from apps.endpoints.views import MLAlgorithmViewset
from apps.endpoints.views import MLAlgorithmStatusViewset
from apps.endpoints.views import MLRequestViewset

router = DefaultRouter(trailing_slash=False)
router.register(r"endpoints", EndpointViewset, basename='endpoints')
router.register(r"mlalgorithms", EndpointViewset, basename='mlalgorithms')
router.register(r"mlalgorithmstatuses", EndpointViewset,
                basename='mlalgorithmstatuses')
router.register(r"mlrequests", EndpointViewset, basename='mlrequests')

urlpatterns = [url(r"^api/v1/", include(router.urls))]
