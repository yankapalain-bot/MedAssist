from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

app_name = "clinic"


urlpatterns = [

    # -----------------------------------------------------------------------------------------------------
    # Auth Routes
    # -----------------------------------------------------------------------------------------------------
    
    path("login/",  auth_views.LoginView.as_view(template_name="clinic/login.html"),  name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),



    # -----------------------------------------------------------------------------------------------------
    # Patient Routes
    # -----------------------------------------------------------------------------------------------------
   
    path("patients/",                   views.PatientListView.as_view(),   name="patient_list"),
    path("patients/new/",               views.PatientCreateView.as_view(), name="patient_create"),
    path("patients/<int:pk>/",          views.PatientDetailView.as_view(), name="patient_detail"),
    path("patients/<int:pk>/edit/",     views.PatientUpdateView.as_view(), name="patient_update"),
    path("patients/<int:pk>/delete/",   views.PatientDeleteView.as_view(), name="patient_delete"),

    # --------------------------------------------------------------------------------------------------------------------
    # # Patient - MedicalHistory Routes
    # ---------------------------------------------------------------------------------------------------------------------

    path("medical-history/new/",           views.MedicalHistoryCreateView.as_view(), name="medicalhistory_create"),
    path("medical-history/<int:pk>/edit/", views.MedicalHistoryUpdateView.as_view(), name="medicalhistory_update"), 

    # -------------------------------------------------------------------------------------------------
    # # Patient - Appointment Routes
    # ------------------------------------------------------------------------------------------------- 

    path("appointments/",                   views.AppointmentListView.as_view(),    name="appointment_list"),
    path("appointments/new/",               views.AppointmentCreateView.as_view(),  name="appointment_create"),
    path("appointments/<int:pk>/",          views.AppointmentDetailView.as_view(),  name="appointment_detail"),
    path("appointments/<int:pk>/edit/",     views.AppointmentUpdateView.as_view(),  name="appointment_update"),
    path("appointments/<int:pk>/delete/",   views.AppointmentDeleteView.as_view(),  name="appointment_delete"),

    # ---------------------------------------------------------------------------------------------------------------------
    # # Patient - PregnancyProfile Routes
    # ---------------------------------------------------------------------------------------------------------------------
    
    path("pregnant/new/",           views.PregnancyProfileCreateView.as_view(),   name="pregnancy_create"),
    path("pregnant/<int:pk>/edit/", views.PregnancyProfileUpdateView.as_view(),   name="pregnancy_update"),

    # ---------------------------------------------------------------------------------------------------------------------
    # # Clinical - ConsultationNote Routes
    # ---------------------------------------------------------------------------------------------------------------------

    path("notes/",                  views.ConsultationNoteListView.as_view(),   name="consultationnote_list"),
    path("notes/new/",              views.ConsultationNoteCreateView.as_view(), name="consultationnote_create"),
    path("notes/<int:pk>/",         views.ConsultationNoteDetailView.as_view(), name="consultationnote_detail"),
    path("notes/<int:pk>/edit",     views.ConsultationNoteUpdateView.as_view(), name="consultationnote_update"),
    path("notes/<int:pk>/delete",   views.ConsultationNoteDeleteView.as_view(), name="consultationnote_delete"),
   
    # ---------------------------------------------------------------------------------------------------------------------
    # # Follow-up reminder Routes
    # ---------------------------------------------------------------------------------------------------------------------

    path("reminders/",                  views.FollowUpReminderListView.as_view(),   name="followupreminder_list"),
    path("reminders/new/",              views.FollowUpReminderCreateView.as_view(), name="followupreminder_create"),
    path("reminders/<int:pk>/",         views.FollowUpReminderDetailView.as_view(), name="followupreminder_detail"),
    path("reminders/<int:pk>/edit",     views.FollowUpReminderUpdateView.as_view(), name="followupreminder_update"),
    path("reminders/<int:pk>/delete",   views.FollowUpReminderDeleteView.as_view(), name="followupreminder_delete"),


    # ---------------------------------------------------------------------------------------------------------------------
    #  User Management Routes
    # ---------------------------------------------------------------------------------------------------------------------

    path("users/",                     views.UserListView.as_view(),   name="user_list"),
    path("users/new/",                 views.UserCreateView.as_view(), name="user_create"),
    path("users/<int:pk>/",            views.UserDetailView.as_view(), name="user_detail"),
    path("users/<int:pk>/edit/",       views.UserUpdateView.as_view(), name="user_update"),
    path("users/<int:pk>/delete/",     views.UserDeleteView.as_view(), name="user_delete"),

    # ---------------------------------------------------------------------------------------------------------------------
    #  Dashboard 
    # ---------------------------------------------------------------------------------------------------------------------

    path("", views.DashboardView.as_view(), name="dashboard"),
]

