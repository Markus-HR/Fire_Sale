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

    def disable_fields(self):
        for field in self.fields:
            self.fields[field].widget.attrs['readonly'] = True
