from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

app_name = "clinic"


urlpatterns = [
   
   # -----------------------------------------------------------------------------------------------------
   # Patient routes
   # -----------------------------------------------------------------------------------------------------
   
    path("patients/",                   views.PatientListView.as_view(),   name="patient_list"),
    path("patients/new/",               views.PatientCreateView.as_view(), name="patient_create"),
    path("patients/<int:pk>/",          views.PatientDetailView.as_view(), name="patient_detail"),
    path("patients/<int:pk>/edit/",     views.PatientUpdateView.as_view(), name="patient_update"),
    path("patients/<int:pk>/delete/",   views.PatientDeleteView.as_view(), name="patient_delete"),

    
]

