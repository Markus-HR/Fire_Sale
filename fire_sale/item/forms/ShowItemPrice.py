from django import forms
from catalogue.models import Bids


class ItemPriceForm(forms.ModelForm):
    class Meta:
        model = Bids
        fields = ['price']

    price = forms.FloatField(
        label='Price',
        widget=forms.TextInput(
            attrs={'name': 'bid_price',
                   'placeholder': 'First name',
                   'style': 'width: 18rem;'
                            'display: block;'
                            'margin : 0 auto;',
                   'class': 'form-control'}))

    def disable_fields(self):
        for field in self.fields:
            self.fields[field].widget.attrs['readonly'] = True
