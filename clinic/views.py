from collections import Counter
from datetime import timedelta


from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.db.models import Count
from django.urls import reverse_lazy
from django.utils import timezone

from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    TemplateView,
    UpdateView,
)

from .forms import(
    PatientForm,    
    MedicalHistoryForm,
    AppointmentForm,
    PregnancyProfileForm,
    ConsultationNoteForm,
    ClinicalNoteTemplateForm,
    FollowUpReminderForm,
    StaffProfileForm,
    StaffUserCreationForm,
    StaffUserUpdateForm,
)

from .mixins import HtmxTemplateMixin, SearchableListMixin, StaffRequiredMixin

from .models import (
    Patient,
    StaffProfile,
    MedicalHistory,
    Appointment,
    PregnancyProfile,
    ConsultationNote,
    ClinicalNoteTemplate,
    FollowUpReminder,
)
# Create your views here.

# ----------------------------------------------------------------------------
# Auth Views
# ----------------------------------------------------------------------------


# ----------------------------------------------------------------------------
# Patient Views
# ----------------------------------------------------------------------------

class PatientListView(LoginRequiredMixin, HtmxTemplateMixin, SearchableListMixin, ListView):
    model = Patient    
    paginate_by = 15
    template_name = "clinic/patients/patient_list.html"
    partial_template_name = "clinic/includes/patient_rows.html"
    search_fields = ("first_name", "last_name", "phone", "city", "occupation")


class PatientDetailView(LoginRequiredMixin, DetailView):
    model = Patient
    template_name = "clinic/patients/patient_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        patient = self.object
        context["consultations"] = (
            patient.consultations.select_related("clinician").order_by("-consultation_date")[:10]
        )
        context["appointments"] = (
            patient.appointments.select_related("clinician").order_by("-start_at")[:10]
        )
        context["followups"] = patient.followups.order_by("due_date")[:10]
        
        try:
            context["pregnancy_profile"] = patient.pregnancy_profile
        except PregnancyProfile.DoesNotExist:
            context["pregnancy_profile"] = None
        
        try:
            context["medical_history"] = patient.medical_history
        except MedicalHistory.DoesNotExist:
            context["medical_history"] = None

        return context


class PatientCreateView(LoginRequiredMixin, CreateView):
    model = Patient
    form_class = PatientForm    

    def form_valid(self, form):
        messages.success(self.request, f"Patient {form.instance} created successfully.")
        return super().form_valid(form)


class PatientUpdateView(LoginRequiredMixin, UpdateView):
    model = Patient
    form_class = PatientForm

    def form_valid(self, form):
        messages.success(self.request, f"Patient {form.instance} updated.")
        return super().form_valid(form)


class PatientDeleteView(LoginRequiredMixin, DeleteView):
    model = Patient
    template_name = "clinic/patients/patient_confirm_delete.html"
    success_url = reverse_lazy("clinic:patient_list")


# ----------------------------------------------------------------------------
# # Patient - MedicalHistory Views
# ----------------------------------------------------------------------------

class MedicalHistoryCreateView(LoginRequiredMixin, CreateView):
    model = MedicalHistory
    form_class = MedicalHistoryForm

    def get_initial(self):
        patient_pk = self.request.GET.get("patient")
        if patient_pk:
            return {"patient": patient_pk}
        return {}

    def form_valid(self, form):
        messages.success(self.request, "Patient Medical History saved.")
        return super().form_valid(form)


class MedicalHistoryUpdateView(LoginRequiredMixin, UpdateView):
    model = MedicalHistory
    form_class = MedicalHistoryForm

    def form_valid(self, form):
        messages.success(self.request, "Patient Medical History updated.")
        return super().form_valid(form)



# -------------------------------------------------------------------------------------------------
# # Patient - Appointment Views
# -------------------------------------------------------------------------------------------------

class AppointementListView(LoginRequiredMixin, HtmxTemplateMixin, SearchableListMixin, ListView):
    model = Appointment
    paginate_by = 15
    partial_template_name = "clinic/includes/appointment_rows.html"
    search_fields = ("patient__first_name", "patient__last_name", "purpose", "location")

    def get_queryset(self):
        return(
            super().get_queryset()
            .select_related("patient", "clinician")
            .order_by("start_at")
        )


class AppointmentDetailView(LoginRequiredMixin, DetailView):
    model = Appointment


class AppointmentCreateView(LoginRequiredMixin, DetailView):
    model = Appointment
    form_class = AppointmentForm

    def get_initial(self):
        return {"clinician": self.request.user.pk}
    
    def form_valid(self, form):
        messages.success(self.request, "Appointment schedules.")
        return super().form_valide(form)


class AppointmentUpdateView(LoginRequiredMixin, UpdateView):
    model = Appointment
    form_class = AppointmentForm


class AppointmentDeleteView(LoginRequiredMixin, DeleteView):
    model = Appointment
    success_url = reverse_lazy("clinic:Appointment_list")



# -------------------------------------------------------------------------------------------------
# # Patient - PregnancyProfile Views
# -------------------------------------------------------------------------------------------------

class PregnancyProfileCreateView(LoginRequiredMixin, CreateView):
    model = PregnancyProfile
    form_class = PregnancyProfileForm

    def get_initial(self):
        patient_pk = self.request.GET.get("patient")
        if patient_pk:
            return {"patient": patient_pk}
        return{}


class PregnancyProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = PregnancyProfile
    form_class = PregnancyProfileForm


# ---------------------------------------------------------------------------------------------------------
# # Clinical - ConsultationNote Views
# ---------------------------------------------------------------------------------------------------------

class ConsultationNoteListView(LoginRequiredMixin, HtmxTemplateMixin, SearchableListMixin, ListView):

    model = ConsultationNote
    paginate_by = 15
    partial_template_name = "clinic/includes/consultationnote_rows.html"
    search_fields = ("patient__first_name", "patient__last_name", "reason_for_visit", "assessment")

    def get_queryset(self):
        return (
            super().get_queryset()
            .select_related("patient", "clinician", "template")
            .order_by("-consultation_date")
        )


class ConsultationNoteDetailView(LoginRequiredMixin, DetailView):
    model = ConsultationNote


class ConsultationNoteCreateView(LoginRequiredMixin, CreateView):
    model = ConsultationNote
    form_class = ConsultationNoteForm

    def get_initial(self):
        patient_pk = self.request.GET.get("patient")
        if patient_pk:
            return {"patient": patient_pk, "clinician": self.request.user.pk}
        return {"clinician": self.request.user.pk}
    
    def form_valid(self, form):
        messages.success(self.request, "Consultation notes saved.")
        return super().form_valid(form)


class ConsultationNoteUpdateView(LoginRequiredMixin, UpdateView):
    model = ConsultationNote
    form_class = ConsultationNoteForm


class ConsultationNoteDeleteView(LoginRequiredMixin, DeleteView):
    model = ConsultationNote
    success_url = reverse_lazy("clinic:consultationnote_list")



# ---------------------------------------------------------------------------------------------------------
# # Follow-up reminder Views
# ---------------------------------------------------------------------------------------------------------

class FollowUpReminderListView(LoginRequiredMixin, HtmxTemplateMixin, SearchableListMixin, ListView):
    model = FollowUpReminder
    paginate_by = 15
    partial_template_name = "clinic/includes/followupreminder_rows.html"
    search_fields = ("patient__first_name", "patient__last_name", "title", "status")

    def get_queryset(self):
        return (
            super().get_queryset()
            .select_related("patient", "appointment")
            .order_by("due_date")
        )


class FollowUpReminderDetailView(LoginRequiredMixin, DeleteView):
    model = FollowUpReminder
    

class FollowUpReminderCreateView(LoginRequiredMixin, CreateView):
    model = FollowUpReminder
    form_class = FollowUpReminderForm

    def form_valid(self, form):
        messages.success(self.request, "Follow-up reminder created.")
        return super().form_valide(form)


class FollowUpReminderUpdateView(LoginRequiredMixin, UpdateView):
    model = FollowUpReminder
    form_class = FollowUpReminderForm


class FollowUpReminderDeleteView(LoginRequiredMixin, DeleteView):
    model = FollowUpReminder
    success_url = reverse_lazy("clinic:followupreminder_list")

    

# ---------------------------------------------------------------------------------------------------------------------
#  User Management Views
# ---------------------------------------------------------------------------------------------------------------------
    
class UserListView(StaffRequiredMixin, HtmxTemplateMixin, SearchableListMixin, ListView):
    model = User
    paginate_by = 15
    partial_template_name = "clinic/includes/user_rows.html"
    search_fields = ("username", "first_name", "last_name", "email")
    template_name = "clinic/users/user_list.html"


    def get_queryset(self):
        return super().get_queryset().order_by("username")


class UserDetailView(LoginRequiredMixin, DetailView): 
    model = User
    template_name = "clinic/users/user_detail.html"
    context_object_name = "profile_user"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            context["staff_profile"] = self.object.staff_profile
        except StaffProfile.DoesNotExist:
            context["staff_profile"] = None
        return context


class UserCreateView(StaffRequiredMixin, CreateView):
    model = User
    form_class = StaffUserCreationForm
    template_name = "clinic/users/user_form.html"
    success_url = reverse_lazy("clinic:user_list")

    def form_valid(self, form):
        response = super().form_valid(form)
        # Save groups after the user is created (M2M requires a saved object)
        self.object.groups.set(form.cleaned_data["groups"])
        # Create an empty StaffProfile for the new user
        StaffProfile.objects.get_or_create(user=self.object)
        messages.success(self.request, f"User {self.object.username} created.")
        return response


class UserUpdateView(StaffRequiredMixin, UpdateView):
    model = User
    form_class = StaffUserUpdateForm
    template_name = "clinic/users/user_form.html"
    success_url = reverse_lazy("clinic:user_list")

    def form_valid(self, form):
        response = super().form_valid(form)
        self.object.groups.set(form.cleaned_data["groups"])
        messages.success(self.request, f"User {self.object.username} updated.")
        return response


class UserDeleteView(StaffRequiredMixin, DeleteView):
    model = User
    template_name = "clinic/users/user_confirm_delete.html"
    success_url = reverse_lazy("clinic:user_list")
