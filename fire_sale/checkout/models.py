from django.db import models
from catalogue.models import Postings


class Country(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Contacts(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    street_name = models.CharField(max_length=100)
    street_no = models.IntegerField()
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    post_code = models.CharField(max_length=100)


class Payments(models.Model):
    name = models.CharField(max_length=100)
    card_no = models.IntegerField()
    expiration_date = models.DateField()
    cvc = models.CharField(max_length=3)


class Orders(models.Model):
    posting = models.ForeignKey(Postings, on_delete=models.CASCADE)
    contact = models.ForeignKey(Contacts, on_delete=models.CASCADE)
    payment = models.ForeignKey(Payments, on_delete=models.CASCADE)

