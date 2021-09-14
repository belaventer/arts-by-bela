from .models import Resolution, Size


def resolution_size_data(request):
    """
    Query all Resolutions and Sizes on database and dump as JSON
    serializable data
    """
    resolutions = Resolution.objects.all()
    sizes = Size.objects.all()

    context = {
        'json_data': {
            'resolutions': list(resolutions.values()),
            'sizes': list(sizes.values())
        },
    }

    return context
