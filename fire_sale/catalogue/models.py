from django.contrib.auth.models import User
from django.db import models
from item.models import Items


class Postings(models.Model):
    item = models.ForeignKey(Items, on_delete=models.CASCADE)
    open = models.BooleanField()
    creation_date = models.DateTimeField()

    def __str__(self):
        return f"{self.item_id, self.open, self.creation_date}"


class Bids(models.Model):
    posting = models.ForeignKey(Postings, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    price = models.FloatField()
    accept = models.BooleanField()


class Ratings(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    posting = models.ForeignKey(Postings, on_delete=models.CASCADE)
    rating = models.IntegerField()