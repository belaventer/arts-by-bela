from django import template

register = template.Library()


# Custom Split Filter from
# https://stackoverflow.com/questions/41932634/
# how-to-split-the-string-in-django-template
# Note - filter is no longer being used, but left in code intentionally.
@register.filter(name='split')
def split(value, key):
    """
        Returns the value turned into a list.
    """
    return value.split(key)
