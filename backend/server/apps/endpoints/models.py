from django.db import models

# Create your models here.


class Endpoint(models.Model):

    name = models.CharField(max_length=128)
    owner = models.CharField(max_length=128)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return self.name


class MLAlgorithm(models.Model):

    name = models.CharField(max_length=128)
    description = models.CharField(max_length=1000)
    code = models.CharField(max_length=50000)
    version = models.CharField(max_length=128)
    owner = models.CharField(max_length=128)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    parent_endpoint = models.ForeignKey(Endpoint, on_delete=models.CASCADE)

    def __str__(self):
        return self.parent_endpoint.name + ' - ' + self.name + ' - ' + self.version


class MLAlgorithmStatus(models.Model):

    status_choices = [('testing', 'testing'),
                      ('staging', 'staging'),
                      ('production', 'production'),
                      ('ab_testing', 'ab_testing')]
    status = models.CharField(max_length=128, choices=status_choices)
    active = models.BooleanField()
    created_by = models.CharField(max_length=128)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    parent_mlalgorithm = models.ForeignKey(MLAlgorithm,
                                           on_delete=models.CASCADE)

    def __str__(self):
        return self.parent_mlalgorithm.name


class MLRequest(models.Model):

    input_data = models.CharField(max_length=10000)
    full_response = models.CharField(max_length=10000)
    response = models.CharField(max_length=10000)
    feedback = models.CharField(max_length=10000)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    parent_mlalgorithm = models.ForeignKey(MLAlgorithm,
                                           on_delete=models.CASCADE)

    def __str__(self):
        return self.parent_mlalgorithm.name
