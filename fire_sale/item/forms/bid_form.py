from django.forms import ModelForm, widgets
from catalogue.models import Bids


class BidCreateForm(ModelForm):
    class Meta:
        model = Bids
        exclude = ['id', 'accept', 'posting_id_id', 'user_id_id']
        widgets = {
            'price': widgets.TextInput(attrs={'class': 'form-control'})
        }
