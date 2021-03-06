from django import forms
from django.core.validators import MinLengthValidator, MaxLengthValidator
from catalogue.models import Ratings
from checkout.models import Payments, Country
from django.db.transaction import commit
from checkout.models import Contacts


# class CheckoutContact(forms.Form):
#     first_name = forms.CharField(
#         label='First name',
#         required=False,
#         widget=forms.TextInput(
#             attrs={'placeholder': 'First name',
#                    'style': 'width: 300px;'
#                             'display: block;'
#                             'margin : 0 auto;',
#                    'class': 'form-control'}))
#
#     last_name = forms.CharField(
#         label='Last name',
#         required=False,
#         widget=forms.TextInput(
#             attrs={'placeholder': 'Last name',
#                    'style': 'width: 300px;'
#                             'display: block;'
#                             'margin : 0 auto;',
#                    'class': 'form-control'}))
#
#     street_name = forms.CharField(
#         label='Street name',
#         required=False,
#         widget=forms.TextInput(
#             attrs={'placeholder': 'Street name',
#                    'style': 'width: 300px;'
#                             'display: block;'
#                             'margin : 0 auto;',
#                    'class': 'form-control'}))
#
#     street_no = forms.CharField(
#         label='Street Number',
#         required=False,
#         widget=forms.TextInput(
#             attrs={'placeholder': 'Street Number',
#                    'style': 'width: 300px;'
#                             'display: block;'
#                             'margin : 0 auto;',
#                    'class': 'form-control'}))
#
#     country = forms.ModelChoiceField(
#         queryset=Country.objects.all(),
#         label='Country',
#         required=False,
#         widget=forms.Select(
#             attrs={'placeholder': 'Country',
#                    'style': 'width: 300px;'
#                             'display: block;'
#                             'margin : 0 auto;',
#                    'class': 'form-control'}))
#
#     post_code = forms.CharField(
#         label='Postal code',
#         required=False,
#         widget=forms.TextInput(
#             attrs={'placeholder': 'Postal code',
#                    'style': 'width: 300px;'
#                             'display: block;'
#                             'margin : 0 auto;',
#                    'class': 'form-control'}))
#
#     def get_data_dict(self):
#         contact_dict = {'first_name': self.data['first_name'],
#                         'last_name': self.data['last_name'],
#                         'street_name': self.data['street_name'],
#                         'street_no': self.data['street_no'],
#                         'country': self.data['country'],
#                         'post_code': self.data['post_code']}
#         return contact_dict
#
#     def read_from_dict(self, contact_dict):
#         self.fields['first_name'].initial = contact_dict['first_name']
#         self.fields['last_name'].initial = contact_dict['last_name']
#         self.fields['street_name'].initial = contact_dict['street_name']
#         self.fields['street_no'].initial = contact_dict['street_no']
#         self.fields['country'].initial = contact_dict['country']
#         self.fields['post_code'].initial = contact_dict['post_code']
#
#
# class CheckoutPayment(forms.Form):
#     name = forms.CharField(
#         label='Name',
#         required=False,
#         widget=forms.TextInput(
#             attrs={'placeholder': 'Name',
#                    'style': 'width: 300px;'
#                             'display: block;'
#                             'margin : 0 auto;',
#                    'class': 'form-control'}))
#
#     card_no = forms.CharField(
#         label='Card number',
#         required=False,
#         widget=forms.TextInput(
#             attrs={'placeholder': 'Card number',
#                    'style': 'width: 300px;'
#                             'display: block;'
#                             'margin : 0 auto;',
#                    'class': 'form-control'}))
#
#     expiration_date = forms.DateField(
#         label='Expiration date',
#         required=False,
#         widget=forms.SelectDateWidget(
#             empty_label=("Choose Year", "Choose Month", "Choose Day"),
#             attrs={'placeholder': 'Expiration date',
#                    'style': 'width: 300px;'
#                             'display: block;'
#                             'margin : 0 auto;',
#                    'class': 'form-control'}))
#
#     cvc = forms.CharField(
#         label='cvc',
#         required=False,
#         widget=forms.TextInput(
#             attrs={'placeholder': 'cvc',
#                    'style': 'width: 300px;'
#                             'display: block;'
#                             'margin : 0 auto;',
#                    'class': 'form-control'}))
#
#     def get_data_dict(self):
#         payment_dict = {'name': self.data['name'],
#                         'card_no': self.data['card_no'],
#                         'expiration_date': f"{self.data['expiration_date_year']}-" +
#                                            f"{self.data['expiration_date_month']}-" +
#                                            f"{self.data['expiration_date_day']}",
#                         'cvc': self.data['cvc']}
#         return payment_dict
#
#     def read_from_dict(self, payment_dict):
#         self.fields['name'].initial = payment_dict['name']
#         self.fields['card_no'].initial = payment_dict['card_no']
#         self.fields['expiration_date'] = payment_dict['expiration_date']
#         self.fields['cvc'].initial = payment_dict['cvc']
#
#
class RatingForm(forms.Form):
    rating = forms.ChoiceField(
        label='Rating',
        required=False,
        widget=forms.RadioSelect(attrs={}),
        choices=((1, "1"),
                 (2, "2"),
                 (3, "3"),
                 (4, "4"),
                 (5, "5")))

    def get_data_dict(self):
        rating_dict = {'rating': self.data.get('rating-rating', None)}
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
            attrs={'name': 'contact_first_name',
                   'placeholder': 'First name',
                   'style': 'width: 300px;'
                            'display: block;'
                            'margin : 0 auto;',
                   'class': 'form-control'}))

    last_name = forms.CharField(
        label='Last name',
        widget=forms.TextInput(
            attrs={'name': 'contact_last_name',
                   'placeholder': 'Last name',
                   'style': 'width: 300px;'
                            'display: block;'
                            'margin : 0 auto;',
                   'class': 'form-control'}))

    street_name = forms.CharField(
        label='Street name',
        widget=forms.TextInput(
            attrs={'name': 'contact_street_name',
                   'placeholder': 'Street name',
                   'style': 'width: 300px;'
                            'display: block;'
                            'margin : 0 auto;',
                   'class': 'form-control'}))

    house_no = forms.CharField(
        label='House Number',
        widget=forms.TextInput(
            attrs={'name': 'contact_house_no',
                   'placeholder': 'House Number',
                   'style': 'width: 300px;'
                            'display: block;'
                            'margin : 0 auto;',
                   'class': 'form-control'}))

    city = forms.CharField(
        label='City',
        widget=forms.TextInput(
            attrs={'name': 'contact_City',
                   'placeholder': 'City',
                   'style': 'width: 300px;'
                            'display: block;'
                            'margin : 0 auto;',
                   'class': 'form-control'}))

    country = forms.ModelChoiceField(
        queryset=Country.objects.all(),
        label='Country',
        widget=forms.Select(
            attrs={'name': 'contact_country',
                   'placeholder': 'Country',
                   'style': 'width: 300px;'
                            'display: block;'
                            'margin : 0 auto;',
                   'class': 'form-control'}))

    post_code = forms.CharField(
        label='Postal code',
        widget=forms.TextInput(
            attrs={'name': 'contact_post_code',
                   'placeholder': 'Postal code',
                   'style': 'width: 300px;'
                            'display: block;'
                            'margin : 0 auto;',
                   'class': 'form-control'}))

    def get_data_dict(self):
        contact_dict = {'first_name': self.data['contact-first_name'],
                        'last_name': self.data['contact-last_name'],
                        'street_name': self.data['contact-street_name'],
                        'house_no': self.data['contact-house_no'],
                        'city': self.data['contact-city'],
                        'country': self.data['contact-country'],
                        'post_code': self.data['contact-post_code']}
        return contact_dict

    def read_from_dict(self, contact_dict):
        self.fields['first_name'] = contact_dict['first_name']
        self.fields['last_name'] = contact_dict['last_name']
        self.fields['street_name'] = contact_dict['street_name']
        self.fields['house_no'] = contact_dict['house_no']
        self.fields['city'] = contact_dict['city']
        self.fields['country'] = contact_dict['country']
        self.fields['post_code'] = contact_dict['post_code']

    def disable_fields(self):
        for field in self.fields:
            self.fields[field].widget.attrs['readonly'] = True

    def not_required_fields(self):
        for field in self.fields:
            self.fields[field].required = False

    def save(self):
        contact = super().save(commit=False)
        contact.country = Country.objects.get(name=self.cleaned_data['country'])
        if commit:
            contact.save()
        return contact


class PaymentReviewForm(forms.ModelForm):
    class Meta:
        model = Payments
        exclude = ['id']

    name = forms.CharField(
        label='Name',
        widget=forms.TextInput(
            attrs={'name': 'payment_name',
                   'placeholder': 'Name',
                   'style': 'width: 18rem;'
                            'display: block;'
                            'margin : 0 auto;',
                   'class': 'form-control'}))

    card_no = forms.CharField(
        label='Card number',
        validators=[MinLengthValidator(16), MaxLengthValidator(16)],
        widget=forms.TextInput(
            attrs={'name': 'payment_card_no',
                   'placeholder': 'Card number',
                   'style': 'width: 18rem;'
                            'display: block;'
                            'margin : 0 auto;',
                   'class': 'form-control'}))

    expiration_date = forms.DateField(
        label='Expiration date',
        widget=forms.SelectDateWidget(
            empty_label=("Choose Year", "Choose Month", "Choose Day"),
            attrs={'name': 'payment_expiration_date',
                   'placeholder': 'Expiration date',
                   'style': 'width: 18rem;'
                            'display: block;'
                            'margin : 0 auto;',
                   'class': 'form-control'}))

    cvc = forms.CharField(
        label='cvc',
        widget=forms.TextInput(
            attrs={'name': 'payment_cvc',
                   'placeholder': 'cvc',
                   'style': 'width: 18rem;'
                            'display: block;'
                            'margin : 0 auto;',
                   'class': 'form-control'}))

    def get_data_dict(self):
        payment_dict = {'name': self.data['payment-name'],
                        'card_no': self.data['payment-card_no'],
                        'expiration_date': f"{self.data['payment-expiration_date_year']}-" +
                                           f"{self.data['payment-expiration_date_month']}-" +
                                           f"{self.data['payment-expiration_date_day']}",
                        'cvc': self.data['payment-cvc']}
        return payment_dict

    def read_from_dict(self, payment_dict):
        self.fields['name'] = payment_dict['name']
        self.fields['card_no'] = payment_dict['card_no']
        self.fields['expiration_date'] = payment_dict['expiration_date']
        self.fields['cvc'] = payment_dict['cvc']

    def disable_fields(self):
        for field in self.fields:
            self.fields[field].widget.attrs['readonly'] = True

    def not_required_fields(self):
        for field in self.fields:
            self.fields[field].required = False


class RatingReviewForm(forms.ModelForm):
    class Meta:
        model = Ratings
        fields = ['rating']
        widgets = {
            'rating': forms.widgets.TextInput(
                attrs={'name': 'rating_rating',
                       'placeholder': 'rating',
                       'style': 'width: 18rem;'
                                'display: block;'
                                'margin : 0 auto;',
                       'class': 'form-control'})}

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
    country = None
    if len(contact_dict['country']) > 0:
        if Country.objects.filter(id=contact_dict['country']).exists():
            country = Country.objects.get(id=contact_dict['country'])
    contact = Contacts(first_name=contact_dict['first_name'],
                       last_name=contact_dict['last_name'],
                       street_name=contact_dict['street_name'],
                       house_no=contact_dict['house_no'],
                       city=contact_dict['city'],
                       country=country,
                       post_code=contact_dict['post_code'])
    return contact


def create_payment_model(payment_dict):
    payment = Payments(name=payment_dict['name'],
                       card_no=payment_dict['card_no'],
                       expiration_date=payment_dict['expiration_date'],
                       cvc=payment_dict['cvc'])
    return payment


def create_rating_model(rating_dict):
    rating = Ratings(rating=rating_dict['rating'])
    return rating
