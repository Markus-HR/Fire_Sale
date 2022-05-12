from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Items(models.Model):
    name = models.CharField(max_length=255)
    condition = models.CharField(max_length=255)
    long_description = models.CharField(max_length=500, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    image1 = models.CharField(max_length=9999)
    image2 = models.CharField(max_length=9999, blank=True)
    image3 = models.CharField(max_length=9999, blank=True)
    image4 = models.CharField(max_length=9999, blank=True)
    image5 = models.CharField(max_length=9999, blank=True)

