from .models import Resolution, Size


def resolution_size_data(request):

    resolutions = Resolution.objects.all()
    sizes = Size.objects.all()

    context = {
        'json_data': {
            'resolutions': list(resolutions.values()),
            'sizes': list(sizes.values())
        },
    }

    return context
