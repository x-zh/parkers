from django.db import models


class Notify(models.Model):

    title = models.CharField(max_length=40)
    lat = models.DecimalField(max_digits=15, decimal_places=8, default=0.0)
    lng = models.DecimalField(max_digits=15, decimal_places=8, default=0.0)
    datetime = models.DateTimeField(auto_now=True)
