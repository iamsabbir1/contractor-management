"""
URL mappings for the user API
"""

from django.urls import path
from contractor import views

app_name = "contractor"

urlpatterns = [
    path("create/", views.CreateContractorView.as_view(), name="create"),
    path("token/", views.CreateTokenView.as_view(), name="token"),
    path("me/", views.ManageContractorView.as_view(), name="me"),
]
