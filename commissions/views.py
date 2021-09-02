from django.shortcuts import render


def new_commission(request):
    """ A view to return the new commission page """
    context = {

    }

    return render(request, 'commissions/new_commission.html', context)
