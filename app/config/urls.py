from django.contrib import admin
from django.urls import path
from policies.views import (
    home, client_list, client_create, client_update, client_delete,
    policy_list, policy_create, policy_update, policy_delete, client_detail, policy_detail
)


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", home, name="home"),
    path("clients/", client_list, name="client-list"),
    path("clients/new/", client_create, name="client-create"),
    path("clients/<int:pk>/edit/", client_update, name="client-update"),
    path("clients/<int:pk>/delete/", client_delete, name="client-delete"),
    path("policies/", policy_list, name="policy-list"),
    path("policies/new/", policy_create, name="policy-create"),
    path("policies/<int:pk>/edit/", policy_update, name="policy-update"),
    path("policies/<int:pk>/delete/", policy_delete, name="policy-delete"),
    path("clients/<int:pk>/", client_detail, name="client-detail"),
    path("policies/<int:pk>/", policy_detail, name="policy-detail"),
]
