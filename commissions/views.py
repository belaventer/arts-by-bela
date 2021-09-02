from django.shortcuts import render
from .forms import CommisionForm


def new_commission(request):
    """ A view to return the new commission page """

    form = CommisionForm()

    context = {
        'form': form,
    }

    return render(request, 'commissions/new_commission.html', context)
