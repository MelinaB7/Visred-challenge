from django.contrib import admin
from django.urls import path
from policies.views import home, client_list, client_create, client_update, client_delete


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", home, name="home"),
    path("clients/", client_list, name="client-list"),
    path("clients/new/", client_create, name="client-create"),
    path("clients/<int:pk>/edit/", client_update, name="client-update"),
     path("clients/<int:pk>/delete/", client_delete, name="client-delete"),
]
