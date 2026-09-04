from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import ProtectedError
from .models import Client
from .forms import ClientForm


def home(request):
    """Placeholder home view. Replace with the real app."""
    return render(request, "home.html")


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