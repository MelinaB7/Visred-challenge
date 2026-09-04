from django.db import models
from django.core.validators import RegexValidator


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

    def __str__(self):
        return f"{self.number} - {self.client.name}"