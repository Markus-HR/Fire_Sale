from django.forms import ModelForm, widgets
from catalogue.models import Bids


class BidCreateForm(ModelForm):
    class Meta:
        model = Bids
        fields = ['price']
        widgets = {
            'price': widgets.TextInput(
                attrs={'class': 'form-control',
                       'placeholder': 'Amount...'})
        }
