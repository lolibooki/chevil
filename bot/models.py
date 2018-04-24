from django.db import models


class Customer(models.Model):
    username = models.CharField(max_length=30)
    # first_name = models.CharField(max_length=250)
    chat_id = models.BigIntegerField()
    name = models.CharField(max_length=50)
    address = models.TextField()
    location_long = models.FloatField()
    location_lat = models.FloatField()
    phone = models.CharField(max_length=11)
    mobile = models.CharField(max_length=11)


