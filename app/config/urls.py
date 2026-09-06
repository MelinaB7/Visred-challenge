from django.contrib import admin
from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from policies.views import (
    home, client_list, client_create, client_update, client_delete,
    policy_list, policy_create, policy_update, policy_delete, client_detail, policy_detail, 
    policy_renew, policy_type_list, policy_type_create, policy_type_update
)


urlpatterns = [
    path("admin/", admin.site.urls),
    path("login/", LoginView.as_view(template_name="login.html"), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
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
    path("policies/<int:pk>/renew/", policy_renew, name="policy-renew"),
    path("policy-types/", policy_type_list, name="policy-type-list"),
    path("policy-types/new/", policy_type_create, name="policy-type-create"),
    path("policy-types/<int:pk>/edit/", policy_type_update, name="policy-type-update"),
]