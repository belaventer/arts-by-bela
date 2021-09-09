from django.shortcuts import render

from commissions.models import Artwork


def showcase(request):
    """ A view to return the showcase of all completed artworks """

    artworks = Artwork.objects.all()

    context = {
        'artworks': artworks,
    }

    return render(request, 'showcase/showcase.html', context)
