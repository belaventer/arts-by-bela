from django import forms
from .models import UserProfile


class UserProfileForm(forms.ModelForm):
    """
    UserProfile Model Form to select and format desired fields for
    profile template
    """
    class Meta:
        model = UserProfile
        exclude = ('user',)

    def __init__(self, *args, **kwargs):
        """
        Add placeholders and classes, remove auto-generated
        labels and set autofocus on first field
        """
        super().__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs['class'] = ('validate')
            self.fields[field].label = False
