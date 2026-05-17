from django.shortcuts import render
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

# ─────────────────────────────────────────────────────────────────────────────
# Patient views
# ─────────────────────────────────────────────────────────────────────────────

# class PatientListView(ListView):
#     model = Patient
#     template_name = "clinic/patient_list.html"
#     paginate_by = 15
#     partial_template_name = "clinic/includes/patient_rows.html"
#     search_fields = ("first_name", "last_name", "phone", "city", "occupation")

class PatientListView(ListView):
    """
    Display searchable paginated patient list.
    Supports HTMX partial rendering.
    """

    model = Patient
    template_name = "clinic/patient_list.html"
    context_object_name = "patients"

    paginate_by = 15
    paginate_orphans = 2

    ordering = ["last_name", "first_name"]

    partial_template_name = "clinic/includes/patient_rows.html"

    search_fields = (
        "first_name",
        "last_name",
        "phone",
        "city",
        "occupation",
    )

    def get_queryset(self):
        return (
            Patient.objects
            .filter(is_active=True)
        )


class PatientDetailView(DetailView):
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
        # Try to get the pregnancy profile (may not exist for male patients or some female patients)
        try:
            context["pregnancy_profile"] = patient.pregnancy_profile
        except PregnancyProfile.DoesNotExist:
            context["pregnancy_profile"] = None
        return context


""" class PatientCreateView(CreateView):
    model = Patient
    form_class = PatientForm

    def form_valid(self, form):
        messages.success(self.request, f"Patient {form.instance} created successfully.")
        return super().form_valid(form)


class PatientUpdateView(UpdateView):
    model = Patient
    form_class = PatientForm

    def form_valid(self, form):
        messages.success(self.request, f"Patient {form.instance} updated.")
        return super().form_valid(form) """


class PatientDeleteView(DeleteView):
    model = Patient
    success_url = reverse_lazy("clinic:patient_list")
    # reverse_lazy: like reverse() but evaluated lazily (at call time, not import time).
    # Use reverse_lazy in class attributes. Use reverse() inside functions.
