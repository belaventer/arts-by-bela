from django.shortcuts import render
from commissions import models


def index(request):
    """ A view to return the home page """
    resolutions = models.Resolution.objects.all()
    sizes = models.Size.objects.all()
    context = {
        'resolutions': resolutions,
        'resolutions_json': list(resolutions.values()),
        'sizes': sizes,
        'sizes_json': list(sizes.values()),
    }

    return render(request, 'home/index.html', context)
