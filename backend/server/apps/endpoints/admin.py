from django.contrib import admin
from apps.endpoints.models import Endpoint
from apps.endpoints.models import MLAlgorithm
from apps.endpoints.models import MLAlgorithmStatus
from apps.endpoints.models import MLRequest
# Register your models here.


class MLAlgorithmStatusAdmin(admin.ModelAdmin):
    list_display = ('parent_mlalgorithm', 'status', 'active')
    list_editable = ('active', 'status')


admin.site.register(Endpoint)
admin.site.register(MLAlgorithm)
admin.site.register(MLAlgorithmStatus, MLAlgorithmStatusAdmin)
admin.site.register(MLRequest)
