""" Account Models """

import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _

from . import utils


class User(AbstractUser):
    """User project models
    Args: AbstractUser (_type_): Abstract user class
    _type_: Model
    """

    USER_TYPE = (("admin", "admin"), ("normal", "normal"))
    uid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    slug = models.SlugField(unique=True)
    email = models.EmailField(_("email address"), unique=True, null=False, blank=False)
    otp = models.CharField(_("otp code"), max_length=100, null=True, blank=True)
    reset_token = models.CharField(_("reset token"), max_length=1000, null=True, blank=True)
    type = models.CharField(_("type"), max_length=8, choices=USER_TYPE, default="normal")

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    class Meta:
        ordering = ["-date_joined", "first_name"]
        verbose_name = _("Utilizador")
        verbose_name_plural = _("Utilizadores")

    def __str__(self) -> str:
        return self.email

    def save(self, *args, **kwargs) -> None:
        email_username, _ = self.email.split("@")

        if not self.last_name:
            self.last_name = ""

        if not self.username:
            self.username = email_username

        if self.is_superuser:
            self.type = "admin"

        if not self.slug:
            self.slug = slugify(f"{self.first_name} {self.last_name} {utils.generate_short_id(4)}")
        return super(User, self).save(*args, **kwargs)


class Area(models.Model):
    """Area models"""

    name = models.CharField(_("name"), max_length=150, null=False, blank=False)
    aid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    description = models.TextField(default="")
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name", "created_at"]
        verbose_name = _("area")
        verbose_name_plural = _("Areas")

    def __str__(self) -> str:
        return str(self.name)


class Employee(models.Model):
    """employees model"""

    bi = models.CharField(max_length=14, null=True, unique=True, blank=True)
    user = models.OneToOneField(verbose_name=_("user"), to=User, on_delete=models.CASCADE, related_name="employee")
    gender = models.CharField(verbose_name=_("gender"), max_length=50, choices=utils.GENDER, default=utils.GENDER[0])
    birthday = models.DateField(verbose_name=_("birthday"), null=True, blank=True)
    area = models.ForeignKey(
        verbose_name=_("area"), to=Area, on_delete=models.SET_NULL, null=True, blank=True, default=""
    )
    image = models.ImageField(verbose_name=_("image"), upload_to="employees", blank=True)
    phone = models.CharField(max_length=20, unique=True, null=True)
    # address = models.CharField(max_length=255, null=True, blank=True)
    created_by = models.ForeignKey(
        verbose_name=_("created_by"),
        to=User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="users_created",
    )
    updated_by = models.ForeignKey(
        verbose_name=_("updated_by"),
        to=User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="users_updated",
    )

    class Meta:
        ordering = ["user"]
        verbose_name = _("Funcionário")
        verbose_name_plural = _("Funcionários")

    def __str__(self) -> str:
        return self.user.get_full_name()

    @property
    def image_url(self) -> str:
        """image url get string property"""
        try:
            url = self.image.url  # pylint: disable=no-member
        except ValueError:
            url = ""
        return url

    def get_full_name(self) -> str:
        """employee  full name"""
        return f"{self.user.get_full_name()}"

    def get_create_by(self) -> str:
        """user who create this employee  in system"""
        return f"{self.created_by.get_full_name()}"

    def get_absolute_url(self):
        """absolute url"""
        return reverse("_detail", kwargs={"pk": self.pk})
