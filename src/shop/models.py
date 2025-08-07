import os
from django.conf import settings
from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.IntegerField()
    is_available = models.BooleanField(default=True)
    image = models.ImageField(upload_to='products/', null=True, blank=True)

    def __str__(self):
        return self.name
    
    @property
    def image_url(self):
        if self.image:  
            path = os.path.join(settings.MEDIA_ROOT, str(self.image))
            if os.path.exists(path):  
                return self.image.url
        return None 