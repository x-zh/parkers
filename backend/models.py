from django.db import models


class Location(models.Model):
    """ Raw data of the locations.
    """
    code = models.CharField(max_length=5, blank=True, default='')
    status = models.CharField(max_length=15, blank=True, default='')
    main_street = models.CharField(max_length=255, blank=True, default='')
    from_street = models.CharField(max_length=255, blank=True, default='')
    to_street = models.CharField(max_length=255, blank=True, default='')
    side = models.CharField(max_length=5, blank=True, default='')


class Sign(models.Model):
    """ Raw data of the signs.
    """
    code = models.CharField(db_index=True, max_length=5, blank=True, default='')
    status = models.CharField(db_index=True, max_length=15, blank=True, default='')
    sequence = models.IntegerField()
    distance = models.IntegerField()
    arrow = models.CharField(max_length=5, blank=True, default='')
    description = models.CharField(max_length=255, blank=True, default='')


class LocationWithLatLng(models.Model):
    """ Locations data with latitude and longitude for each intersection.
    """
    code = models.CharField(max_length=5, blank=True, default='')
    status = models.CharField(max_length=15, blank=True, default='')
    main_street = models.CharField(max_length=255, blank=True, default='')
    from_street = models.CharField(max_length=255, blank=True, default='')
    to_street = models.CharField(max_length=255, blank=True, default='')
    side = models.CharField(max_length=5, blank=True, default='')

    # The latitude and longitude of the intersection between main_street and from_street
    lat_main_from = models.DecimalField(max_digits=15, decimal_places=8, default=0.0)
    lng_main_from = models.DecimalField(max_digits=15, decimal_places=8, default=0.0)

    # The latitude and longitude of the intersection between main_street and to_street
    lat_main_to = models.DecimalField(max_digits=15, decimal_places=8, default=0.0)
    lng_main_to = models.DecimalField(max_digits=15, decimal_places=8, default=0.0)
