from django.db import models
from item.models import Item
from user_profile import User


class Posting(models.Model):
    item_id = models.ForeignKey(Item, on_delete=CASCADE)
    open = models.BooleanField()
    creation_date = DateTimeField()


class Bids(models.Model):
    posting_id = models.ForeignKey(Posting, on_delete=CASCADE)
    user_id = models.ForeignKey(User, on_delete=CASCADE)
    price = models.FloatField()
    accept = models.BooleanField()
