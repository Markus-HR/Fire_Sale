from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE())
    bio = models.CharField(max_length=500, blank=True)
    profile_picture = models.CharField(max_length=9999, blank=True)


class Ratings(models.Model):
    user_id = models.ForeignKey(UserProfile)
    #posting_id = models.ForeignKey(Postings)
    rating = models.IntegerField()
