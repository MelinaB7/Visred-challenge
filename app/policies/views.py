from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import ProtectedError, Q
from .models import Client, Policy, PolicyType
from .forms import ClientForm, PolicyForm, PolicyTypeForm


def home(request):
    """Placeholder home view. Replace with the real app."""
    return render(request, "home.html")

#ABM de Client

def client_list(request):
    clients = Client.objects.all()
    return render(request, "client_list.html", {"clients": clients})


def client_create(request):
    if request.method == "POST":
        form = ClientForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("client-list")
    else:
        form = ClientForm()

    return render(request, "client_form.html", {"form": form})


def client_update(request, pk):
    client = get_object_or_404(Client, pk=pk)

    if request.method == "POST":
        form = ClientForm(request.POST, instance=client)
        if form.is_valid():
            form.save()
            return redirect("client-list")
    else:
        form = ClientForm(instance=client)

    return render(request, "client_form.html", {"form": form})


def client_delete(request, pk):
    client = get_object_or_404(Client, pk=pk)

    if request.method == "POST":
        try:
            client.delete()
            return redirect("client-list")
        except ProtectedError:
            return render(request, "client_confirm_delete.html", {
                "client": client,
                "error": "No se puede eliminar: este cliente tiene pólizas asociadas."
            })

    return render(request, "client_confirm_delete.html", {"client": client})

# ABM de Policy

def policy_list(request):
    for policy in Policy.objects.filter(status=Policy.Status.ACTIVE, is_deleted=False):
        policy.refresh_status()

    policies = Policy.objects.filter(is_deleted=False)

    status = request.GET.get("status")
    if status:
        policies = policies.filter(status=status)

    search = request.GET.get("search")
    if search:
        policies = policies.filter(
            Q(number__icontains=search) | Q(client__name__icontains=search)
        )

    return render(request, "policy_list.html", {"policies": policies})



def policy_create(request):
    if request.method == "POST":
        form = PolicyForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("policy-list")
    else:
        form = PolicyForm()

    return render(request, "policy_form.html", {"form": form})


def policy_update(request, pk):
    policy = get_object_or_404(Policy, pk=pk)

    if request.method == "POST":
        form = PolicyForm(request.POST, instance=policy)
        if form.is_valid():
            form.save()
            return redirect("policy-list")
    else:
        form = PolicyForm(instance=policy)

    return render(request, "policy_form.html", {"form": form})


def policy_delete(request, pk):
    policy = get_object_or_404(Policy, pk=pk)

    if request.method == "POST":
        policy.is_deleted = True
        policy.save()
        return redirect("policy-list")

    return render(request, "policy_confirm_delete.html", {"policy": policy})

# Detalle de Client y Policy

def client_detail(request, pk):
    client = get_object_or_404(Client, pk=pk)
    policies = client.policy_set.all()
    return render(request, "client_detail.html", {"client": client, "policies": policies})


def policy_detail(request, pk):
    policy = get_object_or_404(Policy, pk=pk)
    return render(request, "policy_detail.html", {"policy": policy})


# Renovación de pólizas

def policy_renew(request, pk):
    old_policy = get_object_or_404(Policy, pk=pk)
    new_policy = old_policy.build_renewal()

    if request.method == "POST":
        form = PolicyForm(request.POST, instance=new_policy)
        if form.is_valid():
            form.save()
            old_policy.status = Policy.Status.RENEWED
            old_policy.save()
            return redirect("policy-detail", pk=form.instance.pk)
    else:
        form = PolicyForm(instance=new_policy)

    return render(request, "policy_form.html", {"form": form, "renewing": old_policy})


# ABM de PolicyType

def policy_type_list(request):
    policy_types = PolicyType.objects.all()
    return render(request, "policy_type_list.html", {"policy_types": policy_types})


def policy_type_create(request):
    if request.method == "POST":
        form = PolicyTypeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("policy-type-list")
    else:
        form = PolicyTypeForm()

    return render(request, "policy_type_form.html", {"form": form})


def policy_type_update(request, pk):
    policy_type = get_object_or_404(PolicyType, pk=pk)

    if request.method == "POST":
        form = PolicyTypeForm(request.POST, instance=policy_type)
        if form.is_valid():
            form.save()
            return redirect("policy-type-list")
    else:
        form = PolicyTypeForm(instance=policy_type)

    return render(request, "policy_type_form.html", {"form": form})
