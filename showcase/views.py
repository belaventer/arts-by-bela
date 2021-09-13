from django.shortcuts import render, redirect, reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from commissions import models
from .forms import PersonalWork
from profiles.models import UserProfile


def showcase(request):
    """ A view to return the showcase of all completed artworks """

    artworks = models.Artwork.objects.all()

    context = {
        'artworks': artworks,
    }

    return render(request, 'showcase/showcase.html', context)


@login_required
def personal_work(request):
    """ A view to return the add personal work page """
    if not request.user.is_superuser:
        messages.error(
            request, 'Sorry, only artists can add final artworks')
        return redirect(reverse('showcase'))

    if models.Resolution.objects.count() == 0:
        resolution = models.Resolution.objects.create()
        resolution.save()
    else:
        resolution = models.Resolution.objects.all()[0]

    if models.Size.objects.count() == 0:
        size = models.Size.objects.create()
        size.save()
    else:
        size = models.Size.objects.all()[0]

    if request.method == 'POST':
        form = PersonalWork(request.POST, request.FILES)
        if form.is_valid():
            commission = models.Commission.objects.create(
                user_profile=UserProfile.objects.get(user=request.user),
                name=form.cleaned_data['name'],
                description=form.cleaned_data['description'],
                resolution_price=resolution, size_price=size
            )
            commission.save()
            wip = models.WIP.objects.create(commission=commission)
            wip.save()
            artwork = models.Artwork.objects.create(
                commission=commission,
                client_review=form.cleaned_data['description'],
                final_illustration=form.cleaned_data['illustration'])
            artwork.save()

            return redirect(reverse('showcase'))
        else:
            messages.error(
                request, 'Please ensure the form is valid.')
            form = PersonalWork(request.POST, request.FILES)

    form = PersonalWork()

    context = {
        'form': form,
    }

    return render(request, 'showcase/personal_work.html', context)
