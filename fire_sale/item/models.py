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


class Images(models.Model):
    image = models.CharField(max_length=9999)
    item = models.ForeignKey(Items, on_delete=models.CASCADE)

