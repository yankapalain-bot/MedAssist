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
# Patient Views
# ----------------------------------------------------------------------------

class PatientListView(LoginRequiredMixin, HtmxTemplateMixin, SearchableListMixin, ListView):
    model = Patient    
    paginate_by = 15
    partial_template_name = "clinic/includes/patient_rows.html"
    search_fields = ("first_name", "last_name", "phone", "city", "occupation")


class PatientDetailView(LoginRequiredMixin, DetailView):
    model = Patient

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
    success_url = reverse_lazy("clinic:patient_list")

