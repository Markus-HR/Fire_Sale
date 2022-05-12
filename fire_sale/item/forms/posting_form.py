from django.forms import ModelForm, widgets
from item.models import Items


class ItemCreateForm(ModelForm):
    class Meta:
        model = Items
        fields = [
            'name',
            #'item_picture',
            'condition',
            'long_description',
            'category']
        widgets = {
            'name': widgets.TextInput(
                attrs={'class': 'form-control',
                       'placeholder': 'Item name...'}),

            #'item_picture': widgets.TextInput(
            #    attrs={'class': 'form-control',
            #           'placeholder': 'Picture link...'}),

            'condition': widgets.TextInput(
                attrs={'class': 'form-control',
                       'placeholder': 'Condition of item...'}),

            'long_description': widgets.Textarea(
                attrs={'class': 'form-control',
                       'style': 'height: 6rem;',
                       'placeholder': 'Describe the item...'}),

            'category': widgets.Select(
                attrs={'class': 'form-control',
                       'placeholder': 'Select a category...'})
        }
