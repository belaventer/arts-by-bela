from django import forms
from . import models


class CommisionForm(forms.ModelForm):
    class Meta:
        model = models.Commission
        exclude = ('user_profile', 'order_number', 'order_total')

    resolution_price = forms.ModelChoiceField(
        queryset=None, empty_label=None, to_field_name="resolution")
    size_price = forms.ModelChoiceField(
        queryset=None, empty_label=None, to_field_name="size")

    def __init__(self, *args, **kwargs):
        """
        Add placeholders and classes, remove auto-generated
        labels and set autofocus on first field
        """
        super().__init__(*args, **kwargs)
        self.fields['resolution_price'].queryset = (
            models.Resolution.objects.all())
        self.fields['size_price'].queryset = (
            models.Size.objects.all())
        self.fields['number_characters'].widget.attrs['min'] = 0
        self.fields['number_characters'].widget.attrs['max'] = 6

        for field in self.fields:
            if field == 'description':
                self.fields[field].widget.attrs['class'] = (
                    'materialize-textarea validate')
            else:
                self.fields[field].widget.attrs['class'] = ('validate')
            self.fields[field].label = False
