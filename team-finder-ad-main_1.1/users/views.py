from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render

from .forms import UserLoginForm, UserProfileForm, UserRegistrationForm
from .models import User


def register_view(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("projects:project_list")
    else:
        form = UserRegistrationForm()
    return render(request, "users/register.html", {"form": form})


def login_view(request):
    if request.method == "POST":
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("projects:project_list")
        else:
            form.add_error(None, "Неверный email или пароль")
    else:
        form = UserLoginForm()
    return render(request, "users/login.html", {"form": form})


@login_required
def logout_view(request):
    logout(request)
    return redirect("projects:project_list")


def user_detail_view(request, user_id):
    user_obj = get_object_or_404(User, id=user_id)
    return render(request, "users/user-details.html", {"user": user_obj})


@login_required
def user_edit_view(request):
    if request.method == "POST":
        form = UserProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect("users:user_detail", user_id=request.user.id)
    else:
        form = UserProfileForm(instance=request.user)
    return render(request, "users/edit_profile.html", {"form": form})


@login_required
def change_password_view(request):
    if request.method == "POST":
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            return redirect("users:user_detail", user_id=request.user.id)
    else:
        form = PasswordChangeForm(request.user)
    return render(request, "users/change_password.html", {"form": form})


def participants_list_view(request):
    users = User.objects.filter(is_active=True).order_by("id")

    filter_type = request.GET.get("filter")
    if filter_type and request.user.is_authenticated:
        if filter_type == "owners-of-favorite-projects":
            favorite_projects = request.user.favorites.all()
            users = users.filter(owned_projects__in=favorite_projects).distinct()
        elif filter_type == "owners-of-participating-projects":
            participated = request.user.participated_projects.all()
            users = users.filter(owned_projects__in=participated).distinct()
        elif filter_type == "interested-in-my-projects":
            my_projects = request.user.owned_projects.all()
            users = users.filter(favorites__in=my_projects).distinct()
        elif filter_type == "participants-of-my-projects":
            my_projects = request.user.owned_projects.all()
            users = users.filter(participated_projects__in=my_projects).distinct()

    paginator = Paginator(users, 12)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        "users/participants.html",
        {
            "participants": page_obj,
            "active_filter": filter_type,
        },
    )
