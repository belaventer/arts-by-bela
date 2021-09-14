from django import forms
from . import models


class CommissionForm(forms.ModelForm):
    """
    Commission Model Form to select and format desired fields for
    new_commission and edit_commission templates
    """
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


class IllustrationForm(forms.Form):
    """
    Form to relate with wip_illustration and
    final_illustration fields of WIP and Artwork models
    """
    illustration = forms.ImageField(
        required=True, label=False)

    illustration.widget.attrs.update({'hidden': True})


class CommentForm(forms.Form):
    """
    Form to relate with client_comment and
    client_review fields of WIP and Artwork models
    """
    comment = forms.CharField(
        widget=forms.Textarea, required=True, label=False)

    comment.widget.attrs.update({'class': 'materialize-textarea validate'})
