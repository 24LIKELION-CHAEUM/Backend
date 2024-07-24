from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import Poke
from accounts.models import UserProfile

@login_required
def poke_user(request, user_id):
    to_user = get_object_or_404(User, id=user_id)
    Poke.objects.create(from_user=request.user, to_user=to_user)
    return redirect('poke_page')

@login_required
def poke_page(request):
    query = request.GET.get('q')
    user_profile = get_object_or_404(UserProfile, user=request.user)

    if user_profile.user_type == 'senior':
        related_user_profiles = user_profile.protectors
    else:
        related_user_profiles = user_profile.seniors

    related_users = User.objects.filter(id__in=related_user_profiles.values_list('user_id', flat=True))

    if query:
        users = related_users.filter(username__icontains=query)
    else:
        users = []

    user_poke_counts = {user.id: Poke.objects.filter(to_user=user).count() for user in users}
    last_poked_times = {user.id: Poke.objects.filter(to_user=user).last().timestamp if Poke.objects.filter(to_user=user).exists() else None for user in users}

    return render(request, 'poke/poke_page.html', {
        'users': users,
        'query': query,
        'user_poke_counts': user_poke_counts,
        'last_poked_times': last_poked_times
    })
