"""machines models"""

import uuid

from django.contrib.auth import get_user_model
from django.db import models
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _

User = get_user_model()

# MACHINES_STATES = (
#     ("active", "Ativo"),
#     ("inactive", "Inativo"),
#     ("maintenance", "Manutenção"),
#     ("damaged", "Danificado"),
#     ("needs_repair", "Precisa de reparo"),
#     ("discontinued", "Descontinuado"),
#     ("lost", "Perdido"),
# )


class MachineState(models.Model):
    """Machine state model"""

    mid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(verbose_name=_("name"), max_length=100, unique=True, blank=False)
    created_at = models.DateTimeField(verbose_name=_("created_at"), auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name=_("updated_at"), auto_now=True)

    class Meta:
        verbose_name = _("Estado da Máquina")
        verbose_name_plural = _("Estados da Máquinas")
        ordering = ["name", "created_at"]

    def __str__(self) -> str:
        return f"{self.name}"


class Machine(models.Model):
    """Machine model"""

    mid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(verbose_name=_("name"), max_length=150, null=False, unique=True, blank=False)
    slug = models.SlugField(verbose_name=_("slug"), unique=True)
    description = models.TextField(verbose_name=_("description"), default="")
    purchase_value = models.DecimalField(verbose_name=_("purchase_value"), decimal_places=2, max_digits=7)
    state = models.ForeignKey(
        verbose_name=_("state"), to=MachineState, null=False, blank=False, on_delete=models.PROTECT
    )
    created_by = models.ForeignKey(
        verbose_name=_("created_by"),
        to=User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="machines_created",
    )
    created_at = models.DateTimeField(verbose_name=_("created_at"), auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name=_("updated_at"), auto_now=True)

    class Meta:
        verbose_name = _("Máquina")
        verbose_name_plural = _("Máquinas")
        ordering = ["name", "created_at"]

    def __str__(self) -> str:
        return f"{self.name}"

    def save(self, *args, **kwargs) -> None:
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)
