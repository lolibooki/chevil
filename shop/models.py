from django.db import models
import uuid
from django.utils import timezone
# Create your models here.


class Product(models.Model):
    name = models.CharField(max_length=200, unique=True)
    price = models.PositiveIntegerField()
    count = models.PositiveIntegerField()
    number = models.UUIDField(editable=False, default=uuid.uuid4 , unique=True)
    created = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='images/%Y/%m/%d', blank=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return self.name

