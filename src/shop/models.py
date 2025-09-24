from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.IntegerField()
    is_available = models.BooleanField(default=True)
    image = models.ImageField(upload_to='products/', null=True, blank=True)

    @property
    def image_url(self):
        if self.image:
            return self.image.url
        return None

    def __str__(self):
        return self.name