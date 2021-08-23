from django.shortcuts import render
from commissions import models


def index(request):
    """ A view to return the home page """
    resolutions = models.Resolution.objects.all()
    sizes = models.Size.objects.all()
    context = {
        'resolutions': resolutions,
        'sizes': sizes,
        'json_data': {
            'resolutions': list(resolutions.values()),
            'sizes': list(sizes.values())
        },
    }

    return render(request, 'home/index.html', context)
