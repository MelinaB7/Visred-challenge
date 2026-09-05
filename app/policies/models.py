import datetime
from django.db import models
from django.core.validators import RegexValidator
from django.utils import timezone


class Client(models.Model):
    name = models.CharField(max_length=100)

    email = models.EmailField(unique=True)

    phone = models.CharField(
        max_length=20,
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
    name = models.CharField(max_length=50, unique=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Policy(models.Model):
    class Status(models.TextChoices):
        ACTIVE = "active", "Vigente"
        EXPIRED = "expired", "Vencida"
        RENEWED = "renewed", "Renovada"

    number = models.CharField(max_length=30, unique=True)

    client = models.ForeignKey(Client, on_delete=models.PROTECT)

    policy_type = models.ForeignKey(PolicyType, on_delete=models.PROTECT)

    start_date = models.DateField()

    end_date = models.DateField()

    premium = models.DecimalField(max_digits=10, decimal_places=2)

    status = models.CharField(
        max_length=10,
        choices=Status.choices,
        default=Status.ACTIVE
    )

    is_deleted = models.BooleanField(default=False)


    def refresh_status(self):
        if self.status == self.Status.ACTIVE and self.end_date < timezone.now().date():
            self.status = self.Status.EXPIRED
            self.save()


    def build_renewal(self):
        new_start_date = self.end_date + datetime.timedelta(days=1)
        new_end_date = new_start_date.replace(year=new_start_date.year + 1)
        new_number = f"{self.number}-R-{timezone.now().date().isoformat()}"

        return Policy(
            number=new_number,
            client=self.client,
            policy_type=self.policy_type,
            start_date=new_start_date,
            end_date=new_end_date,
            premium=self.premium,
            status=Policy.Status.ACTIVE,
        )


    def __str__(self):
        return f"{self.number} - {self.client.name}"