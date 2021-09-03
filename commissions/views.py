from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import CommissionForm
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
            return redirect(reverse('profile'))
        else:
            messages.error(
                request, 'Please ensure the form is valid.')

    form = CommissionForm()

    context = {
        'form': form,
    }

    return render(request, 'commissions/new_commission.html', context)
