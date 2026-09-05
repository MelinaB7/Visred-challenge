import datetime
from django.db import models
from django.core.validators import RegexValidator
from django.utils import timezone


class Client(models.Model):
    name = models.CharField(max_length=100, verbose_name="Nombre")

    email = models.EmailField(unique=True, verbose_name="Email")

    phone = models.CharField(
        max_length=20,
        verbose_name="Telefono",
        validators=[
            RegexValidator(
                regex=r'^\+?[\d\s-]+$',
                message="El teléfono solo puede contener números, espacios, guiones y un '+' opcional al inicio."
            )
        ]
    )

    document = models.CharField(
        max_length=20,
        unique=True,
        verbose_name="Documento",
        validators=[
            RegexValidator(
                regex=r'^\d+$',
                message="El documento debe contener solo números."
            )
        ]
    )

    def __str__(self):
        return self.name


class PolicyType(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name="Nombre")
    is_active = models.BooleanField(default=True, verbose_name="Activo")

    def __str__(self):
        return self.name


class Policy(models.Model):
    class Status(models.TextChoices):
        ACTIVE = "active", "Vigente"
        EXPIRED = "expired", "Vencida"
        RENEWED = "renewed", "Renovada"

    number = models.CharField(max_length=10, unique=True, verbose_name="Numero", blank=True)

    client = models.ForeignKey(Client, on_delete=models.PROTECT, verbose_name="Cliente")

    policy_type = models.ForeignKey(PolicyType, on_delete=models.PROTECT, verbose_name="Tipo de Póliza")

    start_date = models.DateField(verbose_name="Fecha de inicio")

    end_date = models.DateField(verbose_name="Fecha de vencimiento")

    premium = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Prima")

    status = models.CharField(
        max_length=10,
        choices=Status.choices,
        default=Status.ACTIVE,
        verbose_name="Estado"
    )

    is_deleted = models.BooleanField(default=False, verbose_name="Eliminada")

    renewed_from = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="renewals",
        verbose_name="Renovada desde"
    )


    def refresh_status(self):
        if self.status == self.Status.ACTIVE and self.end_date < timezone.now().date():
            self.status = self.Status.EXPIRED
            self.save()
            
    @classmethod
    def _generate_next_number(cls, prefix):
        last_policy = (
            cls.objects.filter(number__startswith=prefix)
            .order_by("-number")
            .first()
        )
        if last_policy:
            next_sequence = int(last_policy.number[len(prefix):]) + 1
        else:
            next_sequence = 1

        candidate = f"{prefix}{next_sequence:05d}"
        while cls.objects.filter(number=candidate).exists():
            next_sequence += 1
            candidate = f"{prefix}{next_sequence:05d}"

        return candidate

    def save(self, *args, **kwargs):
        if not self.number:
            prefix = "R" if self.renewed_from else "P"
            self.number = self._generate_next_number(prefix)
        super().save(*args, **kwargs)

    def build_renewal(self):
        new_start_date = self.end_date + datetime.timedelta(days=1)
        new_end_date = new_start_date.replace(year=new_start_date.year + 1)

        return Policy(
            client=self.client,
            policy_type=self.policy_type,
            start_date=new_start_date,
            end_date=new_end_date,
            premium=self.premium,
            status=Policy.Status.ACTIVE,
            renewed_from=self,
        )

    def __str__(self):
        return f"{self.number} - {self.client.name}"