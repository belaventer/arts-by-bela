from django import forms


class PersonalWork(forms.Form):
    """
    Form to get name, description and illustration used
    in the personal_work template.
    """
    name = forms.CharField(
        required=True, label=False, max_length=50)
    description = forms.CharField(
        widget=forms.Textarea, required=True, label=False)
    illustration = forms.ImageField(
        required=True, label=False)

    illustration.widget.attrs.update({'hidden': True})
    description.widget.attrs.update({'class': 'materialize-textarea validate'})
    name.widget.attrs.update({'class': 'validate'})
