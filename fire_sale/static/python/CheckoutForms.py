from django import forms

from catalogue.models import Ratings
from checkout.models import Contacts, Payments, Orders, Country

from checkout.models import Contacts


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

    country = forms.ModelChoiceField(
        queryset=Country.objects.all(),
        label='Country',
        widget=forms.Select(
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

    def get_data_dict(self):
        contact_dict = {'first_name': self.data['first_name'],
                        'last_name': self.data['last_name'],
                        'street_name': self.data['street_name'],
                        'street_no': self.data['street_no'],
                        'country': self.data['country'],
                        'postal_code': self.data['postal_code']}
        return contact_dict

    def read_from_dict(self, contact_dict):
        self.fields['first_name'].initial = contact_dict['first_name']
        self.fields['last_name'].initial = contact_dict['last_name']
        self.fields['street_name'].initial = contact_dict['street_name']
        self.fields['street_no'].initial = contact_dict['street_no']
        self.fields['country'].initial = contact_dict['country']
        self.fields['postal_code'].initial = contact_dict['postal_code']


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
        label='Card number',
        widget=forms.TextInput(
            attrs={'placeholder': 'Card number',
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

    def get_data_dict(self):
        payment_dict = {'name': self.data['name'],
                        'card_no': self.data['card_no'],
                        'expiration_date': self.data['expiration_date'],
                        'cvc': self.data['cvc']}
        return payment_dict

    def read_from_dict(self, payment_dict):
        self.fields['name'].initial = payment_dict['name']
        self.fields['card_no'].initial = payment_dict['card_no']
        self.fields['expiration_date'].initial = payment_dict['expiration_date']
        self.fields['cvc'].initial = payment_dict['cvc']


class RatingForm(forms.Form):
    rating = forms.ChoiceField(
        label='Seller rating',
        required=False,
        widget=forms.RadioSelect(attrs={}),
        choices=((1, "1"),
                 (2, "2"),
                 (3, "3"),
                 (4, "4"),
                 (5, "5")))

    def get_data_dict(self):
        rating_dict = {'rating': self.data.get('rating', None)}
        return rating_dict

    def read_from_dict(self, rating_dict):
        self.fields['rating'].initial = rating_dict['rating']


class ContactReviewForm(forms.ModelForm):
    class Meta:
        model = Contacts
        exclude = ['id']

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

    post_code = forms.CharField(
        label='Postal code',
        widget=forms.TextInput(
            attrs={'placeholder': 'Postal code',
                   'style': 'width: 300px;'
                            'display: block;'
                            'margin : 0 auto;',
                   'class': 'form-control'}))

    def read_from_dict(self, contact_dict):
        self.fields['first_name'] = contact_dict['first_name']
        self.fields['last_name'] = contact_dict['last_name']
        self.fields['street_name'] = contact_dict['street_name']
        self.fields['street_no'] = contact_dict['street_no']
        self.fields['country'] = contact_dict['country']
        self.fields['postal_code'] = contact_dict['postal_code']

    def disable_fields(self):
        for field in self.fields:
            self.fields[field].widget.attrs['readonly'] = True


class PaymentReviewForm(forms.ModelForm):
    class Meta:
        model = Payments
        exclude = ['id']

    name = forms.CharField(
        label='Postal code',
        widget=forms.TextInput(
            attrs={'placeholder': 'Postal code',
                   'style': 'width: 300px;'
                            'display: block;'
                            'margin : 0 auto;',
                   'class': 'form-control'}))

    card_no = forms.CharField(
        label='Card number',
        widget=forms.TextInput(
            attrs={'placeholder': 'Card number',
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

    def read_from_dict(self, payment_dict):
        self.fields['name'] = payment_dict['name']
        self.fields['card_no'] = payment_dict['card_no']
        self.fields['expiration_date'] = payment_dict['expiration_date']
        self.fields['cvc'] = payment_dict['cvc']

    def disable_fields(self):
        for field in self.fields:
            self.fields[field].widget.attrs['readonly'] = True


class RatingReviewForm(forms.ModelForm):
    class Meta:
        model = Ratings
        fields = ['rating']

    rating = forms.ChoiceField(
        label='Seller rating',
        required=False,
        widget=forms.RadioSelect(attrs={}),
        choices=((1, "1"),
                 (2, "2"),
                 (3, "3"),
                 (4, "4"),
                 (5, "5")))

    def get_data_dict(self):
        rating_dict = {'rating': self.data.get('rating', None)}
        return rating_dict

    def read_from_dict(self, rating_dict):
        self.fields['rating'].initial = rating_dict['rating']

    def disable_fields(self):
        for field in self.fields:
            self.fields[field].widget.attrs['readonly'] = True


# Help functions for forms
def create_contact_model(contact_dict):
    contact = Contacts(first_name=contact_dict['first_name'],
                       last_name=contact_dict['last_name'],
                       street_name=contact_dict['street_name'],
                       street_no=contact_dict['street_no'],
                       country=Country.objects.get(id=contact_dict['country']),
                       post_code=contact_dict['postal_code'])
    return contact


def create_payment_model(payment_dict):
    payment = Payments(name=payment_dict['name'],
                       card_no=payment_dict['card_no'],
                       expiration_date=payment_dict['expiration_date'],
                       cvc=payment_dict['cvc'])
    return payment


def create_rating_model(rating_dict, request, posting_id):
    rating = Ratings(user_id=request.user.id,
                     posting=posting_id,
                     rating=rating_dict['rating'])
    return rating
