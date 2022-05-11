from django import forms
from django.utils.safestring import mark_safe


class CheckoutContact(forms.Form):
    first_name = forms.CharField(
        label='First name',
        widget=forms.TextInput(
            attrs={'placeholder': 'First name',
                   'style': 'width: 300px;'
                            'display: block;'
                            'margin : 0 auto;',
                   'class': 'form-control'}))

    last_name = forms.CharField(
        label='Last name',
        widget=forms.TextInput(
            attrs={'placeholder': 'Last name',
                   'style': 'width: 300px;'
                            'display: block;'
                            'margin : 0 auto;',
                   'class': 'form-control'}))

    street_name = forms.CharField(
        label='Street name',
        widget=forms.TextInput(
            attrs={'placeholder': 'Street name',
                   'style': 'width: 300px;'
                            'display: block;'
                            'margin : 0 auto;',
                   'class': 'form-control'}))

    street_no = forms.CharField(
        label='Street Number',
        widget=forms.TextInput(
            attrs={'placeholder': 'Street Number',
                   'style': 'width: 300px;'
                            'display: block;'
                            'margin : 0 auto;',
                   'class': 'form-control'}))

    country = forms.CharField(
        label='Country',
        widget=forms.TextInput(
            attrs={'placeholder': 'Country',
                   'style': 'width: 300px;'
                            'display: block;'
                            'margin : 0 auto;',
                   'class': 'form-control'}))

    postal_code = forms.CharField(
        label='Postal code',
        widget=forms.TextInput(
            attrs={'placeholder': 'Postal code',
                   'style': 'width: 300px;'
                            'display: block;'
                            'margin : 0 auto;',
                   'class': 'form-control'}))


class CheckoutPayment(forms.Form):
    name = forms.CharField(
        label='Postal code',
        widget=forms.TextInput(
            attrs={'placeholder': 'Postal code',
                   'style': 'width: 300px;'
                            'display: block;'
                            'margin : 0 auto;',
                   'class': 'form-control'}))

    card_no = forms.CharField(
        label='Postal code',
        widget=forms.TextInput(
            attrs={'placeholder': 'Postal code',
                   'style': 'width: 300px;'
                            'display: block;'
                            'margin : 0 auto;',
                   'class': 'form-control'}))

    expiration_date = forms.DateField(
        label='Expiration date',
        widget=forms.TextInput(
            attrs={'placeholder': 'Expiration date',
                   'style': 'width: 300px;'
                            'display: block;'
                            'margin : 0 auto;',
                   'class': 'form-control'}))

    cvc = forms.CharField(
        label='cvc',
        widget=forms.TextInput(
            attrs={'placeholder': 'cvc',
                   'style': 'width: 300px;'
                            'display: block;'
                            'margin : 0 auto;',
                   'class': 'form-control'}))


class RatingForm(forms.Form):
    rating = forms.ChoiceField(
        label='Seller rating',
        widget=forms.RadioSelect(attrs={}),
        choices=((1, "1"),
                 (2, "2"),
                 (3, "3"),
                 (4, "4"),
                 (5, "5")))


class ReviewForm(forms.Form):
    pass
