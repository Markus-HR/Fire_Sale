from django import forms
from item.models import Items


class ItemInfoForm(forms.ModelForm):
    class Meta:
        model = Items
        fields = [
            'name',
            "long_description"
        ]

    name = forms.CharField(
        label='Name',
        widget=forms.TextInput(
            attrs={'name': 'item_name',
                   'placeholder': 'First name',
                   'style': 'width: 18rem;'
                            'display: block;'
                            'margin : 0 auto;',
                   'class': 'form-control'}))

    long_description = forms.CharField(
        label='Description',
        widget=forms.Textarea(
            attrs={'name': 'item_description',
                   'placeholder': 'First name',
                   'style': 'width: 18rem;'
                            'display: block;'
                            'margin : 0 auto;',
                   'class': 'form-control'}))

    def disable_fields(self):
        for field in self.fields:
            self.fields[field].widget.attrs['readonly'] = True
