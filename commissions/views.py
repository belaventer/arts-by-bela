from django.shortcuts import (
    render, redirect, reverse, get_object_or_404)
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import CommissionForm, IllustrationForm, CommentForm
from .models import Commission, WIP, Artwork
from profiles.models import UserProfile


@login_required
def new_commission(request):
    """ A view to return the new commission page """

    if request.method == 'POST':
        commission_form = CommissionForm(request.POST, request.FILES)
        if commission_form.is_valid():
            commission = commission_form.save(commit=False)
            commission.user_profile = UserProfile.objects.get(
                user=request.user)
            commission.save()
            return redirect(reverse('payment', args=[commission.id]))
        else:
            messages.error(
                request, 'Please ensure the form is valid.')
            form = CommissionForm(request.POST, request.FILES)

    form = CommissionForm()

    context = {
        'form': form,
    }

    return render(request, 'commissions/new_commission.html', context)


@login_required
def edit_commission(request, commission_id):
    """ A view to return the edit commission page """

    profile = get_object_or_404(UserProfile, user=request.user)
    commission = get_object_or_404(Commission, pk=commission_id)

    if hasattr(commission, 'artwork'):
        return redirect(reverse('artwork', args=[commission_id]))

    if hasattr(commission, 'wip'):
        return redirect(reverse('wip', args=[commission_id]))

    if commission.user_profile != profile:
        messages.error(
            request, 'Sorry, this commission is not yours')
        return redirect(reverse('profile'))

    if request.method == 'POST':
        commission_form = CommissionForm(
            request.POST, request.FILES, instance=commission)
        if commission_form.is_valid():
            commission_form.save()
            messages.success(
                request, 'Commission request updated')
            return redirect(reverse('payment', args=[commission.id]))
        else:
            messages.error(
                request, 'Please ensure the form is valid.')
            form = CommissionForm(
                request.POST, request.FILES, instance=commission)

    form = CommissionForm(instance=commission)

    context = {
        'commission': commission,
        'form': form,
    }

    return render(request, 'commissions/edit_commission.html', context)


@login_required
def delete_commission(request, commission_id):
    """ A view to delete a non paid commission """

    profile = get_object_or_404(UserProfile, user=request.user)
    commission = get_object_or_404(Commission, pk=commission_id)

    if commission.user_profile != profile:
        messages.error(
            request, 'Sorry, this commission is not yours')
        return redirect(reverse('profile'))

    if hasattr(commission, 'wip'):
        messages.error(
            request, 'This commission is already paid')
        return redirect(reverse('profile'))

    commission.reference_image_one.delete()
    commission.reference_image_two.delete()
    commission.reference_image_three.delete()
    commission.reference_image_four.delete()
    commission.reference_image_five.delete()

    commission.delete()
    messages.success(request, 'Commission request deleted!')
    return redirect(reverse('profile'))


@login_required
def wip(request, commission_id):
    """ A view to return the WIP page """

    profile = get_object_or_404(UserProfile, user=request.user)
    commission = get_object_or_404(Commission, pk=commission_id)
    wip = get_object_or_404(WIP, commission=commission)

    if not hasattr(commission, 'wip'):
        messages.error(
            request, 'Please pay your commission request.')
        return redirect(reverse('profile'))

    if not request.user.is_superuser and commission.user_profile != profile:
        messages.error(
            request, 'Sorry, this commission is not yours')
        return redirect(reverse('profile'))

    if request.method == 'POST' and 'illustration' in request.FILES:
        if wip.wip_illustration:
            messages.error(
                request, 'This commission was already sent for comments.')
            return redirect(reverse('wip', args=[commission.id]))

        form = IllustrationForm(request.POST, request.FILES)

        if form.is_valid():
            wip.wip_illustration = form.cleaned_data['illustration']
            wip.save()
            messages.success(
                request, 'Illustration submitted for comments.')
            return redirect(reverse('wip', args=[commission.id]))
        else:
            messages.error(
                request, "Provide a valid image")
            form = IllustrationForm(request.POST, request.FILES)

    if request.method == 'POST' and 'comment' in request.POST:
        if wip.client_comment:
            messages.error(
                request, 'This commission already has a comment.')
            return redirect(reverse('wip', args=[commission.id]))

        form = CommentForm(request.POST)

        if form.is_valid():
            wip.client_comment = form.cleaned_data['comment']
            wip.save()
            Artwork.objects.create(commission=commission)

            messages.success(
                request, 'Comment submitted.')
            return redirect(reverse('profile'))
        else:
            messages.error(
                request, 'Please submit valid comment.')
            form = CommentForm(request.POST)

    form_illustration = IllustrationForm()
    form_comment = CommentForm()

    context = {
        'commission': commission,
        'wip': wip,
        'form_illustration': form_illustration,
        'form_comment': form_comment,
    }

    return render(request, 'commissions/wip_details.html', context)


@login_required
def artwork(request, commission_id):
    """ A view to return the completed artwork page """

    profile = get_object_or_404(UserProfile, user=request.user)
    commission = get_object_or_404(Commission, pk=commission_id)
    wip = get_object_or_404(WIP, commission=commission)
    artwork = get_object_or_404(Artwork, commission=commission)

    if not hasattr(commission, 'wip'):
        messages.error(
            request, 'Please pay your commission request.')
        return redirect(reverse('profile'))

    if not hasattr(commission, 'artwork'):
        messages.error(
            request, 'Sorry, this commission is still in progress.')
        return redirect(reverse('profile'))

    if not request.user.is_superuser and commission.user_profile != profile:
        messages.error(
            request, 'Sorry, this commission is not yours')
        return redirect(reverse('profile'))

    if request.method == 'POST' and 'illustration' in request.FILES:
        if artwork.final_illustration:
            messages.error(
                request, 'This commission is complete.')
            return redirect(reverse('artwork', args=[commission.id]))

        form = IllustrationForm(request.POST, request.FILES)

        if form.is_valid():
            artwork.final_illustration = form.cleaned_data['illustration']
            artwork.save()
            messages.success(
                request, 'Final illustration submitted')
            return redirect(reverse('artwork', args=[commission.id]))
        else:
            messages.error(
                request, "Provide a valid image")
            form = IllustrationForm(request.POST, request.FILES)

    if request.method == 'POST' and 'comment' in request.POST:
        if artwork.client_review:
            messages.error(
                request, 'This commission already has a review.')
            return redirect(reverse('artwork', args=[commission.id]))

        form = CommentForm(request.POST)

        if form.is_valid():
            artwork.client_review = form.cleaned_data['comment']
            artwork.save()

            messages.success(
                request, 'Review submitted.')
            return redirect(reverse('profile'))
        else:
            messages.error(
                request, 'Please submit valid review.')
            form = CommentForm(request.POST)

    form_illustration = IllustrationForm()
    form_comment = CommentForm()

    context = {
        'commission': commission,
        'wip': wip,
        'artwork': artwork,
        'form_illustration': form_illustration,
        'form_comment': form_comment,
    }

    return render(request, 'commissions/artwork_details.html', context)
