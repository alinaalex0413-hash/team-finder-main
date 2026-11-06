from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_http_methods

from .forms import ProjectForm
from .models import Project


def project_list_view(request):
    projects = Project.objects.filter(status="open").order_by("-created_at")

    paginator = Paginator(projects, 12)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        "projects/project_list.html",
        {
            "projects": page_obj,
        },
    )


def project_detail_view(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    return render(
        request,
        "projects/project-details.html",
        {
            "project": project,
            "is_participant": request.user.is_authenticated
            and request.user in project.participants.all(),
        },
    )


@login_required
def project_create_view(request):
    if request.method == "POST":
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.owner = request.user
            project.save()
            project.participants.add(request.user)
            return redirect("projects:project_detail", project_id=project.id)
    else:
        form = ProjectForm()
    return render(
        request,
        "projects/create-project.html",
        {
            "form": form,
            "is_edit": False,
        },
    )


@login_required
def project_edit_view(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    if project.owner != request.user:
        return redirect("projects:project_detail", project_id=project_id)

    if request.method == "POST":
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            return redirect("projects:project_detail", project_id=project_id)
    else:
        form = ProjectForm(instance=project)

    return render(
        request,
        "projects/create-project.html",
        {
            "form": form,
            "is_edit": True,
            "project": project,
        },
    )


@login_required
@require_http_methods(["POST"])
def project_complete_view(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    if project.owner != request.user:
        return JsonResponse(
            {"status": "error", "message": "Недостаточно прав"}, status=403
        )

    if project.status != "open":
        return JsonResponse(
            {"status": "error", "message": "Проект уже завершён"}, status=400
        )

    project.status = "closed"
    project.save()
    return JsonResponse({"status": "ok", "project_status": "closed"})


@login_required
@require_http_methods(["POST"])
def toggle_participate_view(request, project_id):
    project = get_object_or_404(Project, id=project_id)

    if request.user in project.participants.all():
        project.participants.remove(request.user)
        is_participant = False
    else:
        project.participants.add(request.user)
        is_participant = True

    return JsonResponse(
        {
            "status": "ok",
            "participant": is_participant,
            "user_id": request.user.id,
            "user_name": request.user.full_name,
            "user_avatar": (
                request.user.avatar.url
                if request.user.avatar
                else "/static/images/default-avatar.png"
            ),
        }
    )


@login_required
def favorites_list_view(request):
    projects = request.user.favorites.all().order_by("-created_at")
    paginator = Paginator(projects, 12)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, "projects/favorite_projects.html", {"projects": page_obj})


@login_required
@require_http_methods(["POST"])
def toggle_favorite_view(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    if project in request.user.favorites.all():
        request.user.favorites.remove(project)
        favorited = False
    else:
        request.user.favorites.add(project)
        favorited = True

    return JsonResponse({"status": "ok", "favorited": favorited})
