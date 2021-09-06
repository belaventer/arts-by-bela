from django.shortcuts import (
    render, redirect, reverse, get_object_or_404)
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import CommissionForm
from .models import Commission
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

    if commission.user_profile != profile:
        messages.error(
            request, 'Sorry, this commission is not yours')
        return redirect(reverse('profile'))

    if hasattr(commission, 'wip'):
        messages.error(
            request, 'This commission is already paid')
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
