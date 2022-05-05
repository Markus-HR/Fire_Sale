from django.db import models
from item.models import Items
from user_profile.models import UserProfile


class Postings(models.Model):
    item_id = models.ForeignKey(Items, on_delete=models.CASCADE)
    open = models.BooleanField()
    creation_date = models.DateTimeField()
    def __str__(self):
        return f"{self.item_id_id, self.open, self.creation_date}"


class Bids(models.Model):
    posting_id = models.ForeignKey(Postings, on_delete=models.CASCADE)
    user_id = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    price = models.FloatField()
    accept = models.BooleanField()


class Ratings(models.Model):
    user_id = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    posting_id = models.ForeignKey(Postings, on_delete=models.CASCADE)
    rating = models.IntegerField()