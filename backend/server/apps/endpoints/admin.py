from django.contrib import admin
from apps.endpoints.models import Endpoint
from apps.endpoints.models import MLAlgorithm
from apps.endpoints.models import MLAlgorithmStatus
from apps.endpoints.models import MLRequest
# Register your models here.

admin.site.register(Endpoint)
admin.site.register(MLAlgorithm)
admin.site.register(MLAlgorithmStatus)
admin.site.register(MLRequest)
