from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import ProtectedError
from .models import Client, Policy
from .forms import ClientForm, PolicyForm


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
    policies = Policy.objects.all()
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
        policy.delete()
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