from django import forms
from django.core.exceptions import ValidationError

from .models import Project


class ProjectForm(forms.ModelForm):
    def clean_github_url(self):
        url = self.cleaned_data.get("github_url")
        if url and "github.com" not in url:
            raise ValidationError("Ссылка должна вести на GitHub")
        return url

    class Meta:
        model = Project
        fields = ["name", "description", "github_url", "status"]
        widgets = {
            "status": forms.Select(choices=Project.STATUS_CHOICES),
            "description": forms.Textarea(attrs={"rows": 4}),
        }
