from django import forms
from .models import Client, Policy, PolicyType


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ["name", "email", "phone", "document"]


class PolicyForm(forms.ModelForm):
    class Meta:
        model = Policy
        fields = ["client", "policy_type", "start_date", "end_date", "premium"]
        widgets = {
            "start_date": forms.DateInput(attrs={"type": "date"}),
            "end_date": forms.DateInput(attrs={"type": "date"}),
        }
    

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        active_types = PolicyType.objects.filter(is_active=True)

        if self.instance.pk and self.instance.policy_type_id:
            self.fields["policy_type"].queryset = active_types | PolicyType.objects.filter(
                pk=self.instance.policy_type_id
            )
        else:
            self.fields["policy_type"].queryset = active_types


    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get("start_date")
        end_date = cleaned_data.get("end_date")

        if start_date and end_date and start_date >= end_date:
            raise forms.ValidationError("La fecha de inicio debe ser anterior a la fecha de vencimiento.")

        return cleaned_data


class PolicyTypeForm(forms.ModelForm):
    class Meta:
        model = PolicyType
        fields = ["name", "is_active"]

    def clean_name(self):
        name = self.cleaned_data.get("name")
        return name.strip().capitalize()