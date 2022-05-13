from django.forms import ModelForm, widgets
from django import forms
from item.models import Items


class ItemCreateForm(ModelForm):
    class Meta:
        model = Items
        fields = [
            'name',
            'condition',
            'long_description',
            'category',
            'image1',
            'image2',
            'image3',
            'image4',
            'image5',
            ]
        widgets = {
            'name': widgets.TextInput(
                attrs={'class': 'form-control',
                       'placeholder': 'Item name...'}),

            'condition': widgets.TextInput(
                attrs={'class': 'form-control',
                       'placeholder': 'Condition of item...'}),

            'long_description': widgets.Textarea(
                attrs={'class': 'form-control',
                       'style': 'height: 6rem;',
                       'placeholder': 'Describe the item...'}),

            'category': widgets.Select(
                attrs={'class': 'form-control',
                       'placeholder': 'Select a category...'}),

            'image1': widgets.TextInput(
                attrs={'class': 'form-control',
                       'placeholder': 'Image url...'}),

            'image2': widgets.TextInput(
                attrs={'class': 'form-control',
                       'placeholder': 'Optional image url...'}),

            'image3': widgets.TextInput(
                attrs={'class': 'form-control',
                       'placeholder': 'Optional image url...'}),

            'image4': widgets.TextInput(
                attrs={'class': 'form-control',
                       'placeholder': 'Optional image url...'}),

            'image5': widgets.TextInput(
                attrs={'class': 'form-control',
                       'placeholder': 'Optional image url...'}),

        }
