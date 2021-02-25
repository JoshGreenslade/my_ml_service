"""
WSGI config for server project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/wsgi/
"""

from apps.ml.income_classifier.random_forest import RandomForestClassifier
from apps.ml.income_classifier.extra_trees import ExtraTreesClassifier
from apps.ml.registry import MLRegistry
import inspect
import os
from django.core.wsgi import get_wsgi_application
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'server.settings')
application = get_wsgi_application()


try:
    registry = MLRegistry()

    rf = RandomForestClassifier()
    et = ExtraTreesClassifier()

    registry.add_algorithm(endpoint_name="income_classifier",
                           algorithm_object=rf,
                           algorithm_name="random forest",
                           algorithm_status="production",
                           algorithm_version="0.0.1",
                           owner="Josh",
                           algorithm_description="Random forest with simple pre- and post processing",
                           algorithm_code=inspect.getsource(RandomForestClassifier))

    registry.add_algorithm(endpoint_name="income_classifier",
                           algorithm_object=et,
                           algorithm_name="extra trees",
                           algorithm_status="testing",
                           algorithm_version="0.0.1",
                           owner="Josh",
                           algorithm_description="Extra trees with simple pre- and post processing",
                           algorithm_code=inspect.getsource(ExtraTreesClassifier))

except Exception as e:
    print('Exception whilst loading algorithms into the registry', str(e))
