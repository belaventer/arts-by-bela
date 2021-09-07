from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import UserProfile
from .forms import UserProfileForm
from commissions.models import Commission


@login_required
def profile(request):
    """ A view to return the profile page """

    profile = get_object_or_404(UserProfile, user=request.user)
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully')
        else:
            messages.error(request,
                           ('Update failed. Please ensure '
                            'the form is valid.'))
    else:
        form = UserProfileForm(instance=profile)

    if request.user.is_superuser:
        commissions = Commission.objects.filter(
            Q(user_profile__exact=profile) | Q(wip__isnull=False))
    else:
        commissions = profile.commissions.all()

    context = {
        'profile': profile,
        'form': form,
        'commissions': commissions,
    }

    return render(request, 'profiles/profile.html', context)
