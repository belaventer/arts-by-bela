from django import forms
from . import models


class CommissionForm(forms.ModelForm):
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


class WIPForm(forms.ModelForm):
    class Meta:
        model = models.WIP
        exclude = ('commission',)

    def __init__(self, *args, **kwargs):
        """
        Remove labels, add validate class
        and required attributes
        """
        super().__init__(*args, **kwargs)

        self.fields['client_comment'].widget.attrs['class'] = (
            'materialize-textarea validate')
        self.fields['wip_illustration'].widget.attrs['hidden'] = True
        for field in self.fields:
            self.fields[field].required
            self.fields[field].label = False
