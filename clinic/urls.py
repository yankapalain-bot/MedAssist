from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

app_name = "clinic"


urlpatterns = [
       
    # -----------------------------------------------------------------------------------------------------
    # Patient Routes
    # -----------------------------------------------------------------------------------------------------
   
    path("patients/",                   views.PatientListView.as_view(),   name="patient_list"),
    path("patients/new/",               views.PatientCreateView.as_view(), name="patient_create"),
    path("patients/<int:pk>/",          views.PatientDetailView.as_view(), name="patient_detail"),
    path("patients/<int:pk>/edit/",     views.PatientUpdateView.as_view(), name="patient_update"),
    path("patients/<int:pk>/delete/",   views.PatientDeleteView.as_view(), name="patient_delete"),

    # ----------------------------------------------------------------------------
    # # Patient - MedicalHistory Routes
    # ----------------------------------------------------------------------------

    path("medical-history/new/",           views.MedicalHistoryCreateView.as_view(), name="medicalhistory_create"),
    path("medical-history/<int:pk>/edit/", views.MedicalHistoryUpdateView.as_view(), name="medicalhistory_update"), 

    # -------------------------------------------------------------------------------------------------
    # # Patient - Appointment Views
    # ------------------------------------------------------------------------------------------------- 

    path("appointments/",                   views.AppointmentListView.as_view(),    namce="apppointment_list"),
    path("appointments/new/",               views.AppointmentCreateView.as_view(),  name="appointment_create"),
    path("appointments/<int:pk>/",          views.AppointmentDetailView.as_view(),  name="appointment_detail"),
    path("appointments/<int:pk>/edit/",     views.AppointmentUpdateView.as_view(),  name="appointment_update"),
    path("appointments/<int:pk>/delete/",   views.AppointmentDeleteView.as_view,    name="appointment_delete"),
    
    
]

