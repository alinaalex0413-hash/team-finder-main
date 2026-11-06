import random
from io import BytesIO

from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.core.files.base import ContentFile
from django.db import models
from PIL import Image, ImageDraw, ImageFont


class UserManager(BaseUserManager):
    def create_user(self, email, name, surname, password=None, **extra_fields):
        if not email:
            raise ValueError("Email обязателен")
        email = self.normalize_email(email)
        user = self.model(email=email, name=name, surname=surname, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, surname, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        return self.create_user(email, name, surname, password, **extra_fields)


def generate_avatar(name):
    size = (100, 100)
    colors = [
        "#FF6B6B",
        "#4ECDC4",
        "#45B7D1",
        "#96CEB4",
        "#FFEAA7",
        "#DDA0DD",
        "#98D8C8",
        "#F7DC6F",
        "#BB8FCE",
        "#85C1E2",
    ]
    color = random.choice(colors)
    image = Image.new("RGB", size, color)
    draw = ImageDraw.Draw(image)

    try:
        font = ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf", 60)
    except Exception:
        font = ImageFont.load_default()

    text = name[0].upper()
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    position = ((size[0] - text_width) // 2, (size[1] - text_height) // 2)
    draw.text(position, text, fill="white", font=font)

    buffer = BytesIO()
    image.save(buffer, format="PNG")
    return ContentFile(buffer.getvalue(), name=f"avatar_{name}.png")


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, verbose_name="Email")
    name = models.CharField(max_length=124, verbose_name="Имя")
    surname = models.CharField(max_length=124, verbose_name="Фамилия")
    avatar = models.ImageField(upload_to="avatars/", verbose_name="Аватар")
    phone = models.CharField(
        max_length=12, verbose_name="Телефон", default="00000000000"
    )
    github_url = models.URLField(blank=True, null=True, verbose_name="GitHub")
    about = models.TextField(
        max_length=256, blank=True, null=True, verbose_name="О себе"
    )
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    favorites = models.ManyToManyField(
        "projects.Project", related_name="interested_users", blank=True
    )

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name", "surname"]

    def save(self, *args, **kwargs):
        if not self.pk and not self.avatar:
            avatar_file = generate_avatar(self.name)
            self.avatar.save(f"avatar_{self.name}.png", avatar_file, save=False)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} {self.surname}"

    @property
    def full_name(self):
        return f"{self.name} {self.surname}"
