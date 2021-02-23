import json
import numpy

from django.shortcuts import render
from rest_framework import viewsets
from rest_framework import mixins
from rest_framework import views
from rest_framework import status
from rest_framework.response import Response

from apps.endpoints.models import Endpoint
from apps.endpoints.serializers import EndpointSerializer
from apps.endpoints.models import MLAlgorithm
from apps.endpoints.serializers import MLAlgorithmSerializer
from apps.endpoints.models import MLAlgorithmStatus
from apps.endpoints.serializers import MLAlgorithmStatusSerializer
from apps.endpoints.models import MLRequest
from apps.endpoints.serializers import MLRequestSerializer
from apps.ml.registry import MLRegistry
from server.wsgi import registry

# Create your views here.


class EndpointViewset(viewsets.GenericViewSet,
                      mixins.ListModelMixin,
                      mixins.RetrieveModelMixin):
    serializer_class = EndpointSerializer
    queryset = Endpoint.objects.all()


class MLAlgorithmViewset(viewsets.GenericViewSet,
                         mixins.ListModelMixin,
                         mixins.RetrieveModelMixin):
    serializer_class = MLAlgorithmSerializer
    queryset = MLAlgorithm.objects.all()


def deactivate_other_statuses(instance):
    old_statuses = MLAlgorithmStatus.objects.filter(parent_mlalgorithm=instance.parent_mlalgorithm,
                                                    created_at__lt=instance.created_at,
                                                    active=True)
    for i in range(len(old_statuses)):
        old_statuses[i].active = False
    MLAlgorithmStatus.objects.bulk_update(old_statuses, ["active"])


class MLAlgorithmStatusViewset(viewsets.GenericViewSet,
                               mixins.RetrieveModelMixin,
                               mixins.ListModelMixin,
                               mixins.CreateModelMixin,
                               ):
    serializer_class = MLAlgorithmStatusSerializer
    queryset = MLAlgorithmStatus.objects.all()

    def perform_create(self, serializer):
        try:
            with transaction.atomic():
                instance = serializer.save(active=True)
                # set active=False for other statuses
                deactivate_other_statuses(instance)

        except Exception as e:
            raise APIException(str(e))


class MLRequestViewset(viewsets.GenericViewSet,
                       mixins.RetrieveModelMixin,
                       mixins.ListModelMixin,
                       mixins.UpdateModelMixin):
    serializer_class = MLRequestSerializer
    queryset = MLRequest.objects.all()


class PredictView(views.APIView):
    def post(self, request, endpoint_name, format=None):

        algorithm_status = self.request.query_params.get(
            "status", "production")
        algorithm_version = self.request.query_params.get("version")

        algs = MLAlgorithm.objects.filter(
            parent_endpoint__name=endpoint_name, mlalgorithmstatus__status=algorithm_status, mlalgorithmstatus__active=True)

        if algorithm_version is not None:
            algs = algs.filter(version=algorithm_version)

        if len(algs) == 0:
            return Response(
                {"status": "Error", "message": "ML algorithm is not availiable"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        alg_index = 0
        if algorithm_status == "ab_testing":
            alg_index = 0 if np.random.rand() < 0.5 else 1

        algorithm_object = registry.endpoints[algs[alg_index].id]
        prediction = algorithm_object.compute_prediction(request.data)

        label = prediction['label'] if 'label' in prediction else 'error'
        ml_request = MLRequest(
            input_data=json.dumps(request.data),
            full_response=prediction,
            response=label,
            feedback="",
            parent_mlalgorithm=algs[alg_index],
        )
        ml_request.save()

        prediction['request_id'] = ml_request.id

        return Response(prediction)
