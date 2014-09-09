from django.db import models


class Location(models.Model):
    """ Raw data of the locations.
    """
    code = models.CharField(max_length=5, blank=False, default='')
    status = models.CharField(max_length=15, blank=False, default='')
    main_street = models.CharField(max_length=255, blank=False, default='')
    from_street = models.CharField(max_length=255, blank=False, default='')
    to_street = models.CharField(max_length=255, blank=False, default='')
    side = models.CharField(max_length=5, blank=False, default='')


class Sign(models.Model):
    """ Raw data of the signs.
    """
    code = models.CharField(max_length=5, blank=False, default='')
    status = models.CharField(max_length=15, blank=False, default='')
    sequence = models.IntegerField()
    distance = models.IntegerField()
    arrow = models.CharField(max_length=5, blank=False, default='')
    description = models.CharField(max_length=255, blank=False, default='')


class LocationWithLatLng(models.Model):
    """ Locations data with latitude and longitude for each intersection.
    """
    code = models.CharField(max_length=5, blank=False, default='')
    status = models.CharField(max_length=15, blank=False, default='')
    main_street = models.CharField(max_length=255, blank=False, default='')
    from_street = models.CharField(max_length=255, blank=False, default='')
    to_street = models.CharField(max_length=255, blank=False, default='')
    side = models.CharField(max_length=5, blank=False, default='')

    lat_main_from = models.DecimalField(max_digits=15, decimal_places=8, default=0.0)
    lng_main_from = models.DecimalField(max_digits=15, decimal_places=8, default=0.0)

    lat_main_to = models.DecimalField(max_digits=15, decimal_places=8, default=0.0)
    lng_main_to = models.DecimalField(max_digits=15, decimal_places=8, default=0.0)

