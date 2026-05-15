# Business
# Patient, StaffProfile --- include clinician
# MedicalHistory, PregnancyProfile, ClinicalNoteTemplate, ConsultationNote, Appointment, FollowUpReminder
# 
# Help model: TimeStampedModel

from django.conf import settings
from django.db import models
from django.urls import reverse


# ─────────────────────────────────────────────────────────────────────────────
# Help model
# ─────────────────────────────────────────────────────────────────────────────

class TimeStampedModel(models.Model):
    """
    Need to add created_at and updated_at to any model that
    inherits it without write these two fields in every model.
    """
    created_at = models.DateTimeField(auto_now_add=True)
    # auto_now_add=True: set once, when the record is first created. Never changes.

    updated_at = models.DateTimeField(auto_now=True)
    # auto_now=True: updated every time the record is saved.

    class Meta:
        abstract = True


# ─────────────────────────────────────────────────────────────────────────────
# Staff profile
# ─────────────────────────────────────────────────────────────────────────────

class StaffProfile(TimeStampedModel):
    """
    Extra information attached to Django's built-in User model for staff.
    We extend User without replacing it, using a OneToOneField.   
    """
    ROLE_LABELS = [
        ("clinician", "Clinician"),
        ("reception", "Reception"),
        ("manager", "Manager"),
    ]

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="staff_profile",
    )      

    role_label = models.CharField(max_length=20, choices=ROLE_LABELS, default="reception")
    phone = models.CharField(max_length=30, blank=True)
    bio = models.TextField(blank=True)
    avatar_url = models.URLField(blank=True)

    def __str__(self):
        return f"Profile of {self.user.get_full_name() or self.user.username}"

    def get_absolute_url(self):
        return reverse("clinic:user_detail", args=[self.user.pk])


# ─────────────────────────────────────────────────────────────────────────────
# Patient
# ─────────────────────────────────────────────────────────────────────────────

class Patient(TimeStampedModel):
    """
    The central record. Everything else links to this.
    We focus on fields useful for a gynecology clinic.
    """
    SEX_CHOICES = [
        ("F", "Female"),
        ("M", "Male"),
    ]

    first_name = models.CharField(max_length=80)
    last_name = models.CharField(max_length=80)
    sex = models.CharField(max_length=1, choices=SEX_CHOICES)
    date_of_birth = models.DateField(null=True, blank=True)

    phone = models.CharField(max_length=30, blank=True)
    email = models.EmailField(blank=True)
    region = models.CharField(max_length=80, blank=True)
    city = models.CharField(max_length=80, blank=True)
    address = models.CharField(max_length=255, blank=True)
    occupation = models.CharField(max_length=120, blank=True)
    emergency_contact_name = models.CharField(max_length=120, blank=True)
    emergency_contact_phone = models.CharField(max_length=30, blank=True)
    notes = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["last_name", "first_name"]
        # Default ordering: alphabetical by last name.

    def __str__(self):
        return f"{self.last_name} {self.first_name}"        

    def get_absolute_url(self):
        return reverse("clinic:patient_detail", args=[self.pk])        
        # to know where to redirect after a successful form submission.
        # reverse("clinic:patient_detail", args=[self.pk])
        


# ─────────────────────────────────────────────────────────────────────────────
# Medical history
# ─────────────────────────────────────────────────────────────────────────────

class MedicalHistory(TimeStampedModel):
    """
    Stores basic medical background for a patient.    
    One patient has one medical history record.
    """

    patient = models.OneToOneField(
        Patient,
        on_delete=models.CASCADE,
        related_name="medical_history",
    )

    allergies = models.TextField(blank=True)
    chronic_conditions = models.TextField(blank=True)
    medications = models.TextField(blank=True)
    past_surgeries = models.TextField(blank=True)

    def __str__(self):
        return f"Medical history for {self.patient}"

    def get_absolute_url(self):
        return reverse("clinic:patient_detail", args=[self.patient_id])


# ─────────────────────────────────────────────────────────────────────────────
# Pregnancy profile
# ─────────────────────────────────────────────────────────────────────────────

class PregnancyProfile(TimeStampedModel):
    """
    Antenatal data for female patients. Because of Gynecology orientation    
    A patient has at most one pregnancy profile (OneToOneField).
    """
    RISK_LEVELS = [
        ("low", "Low risk"),
        ("moderate", "Moderate risk"),
        ("high", "High risk"),
    ]

    patient = models.OneToOneField(
        Patient,
        on_delete=models.CASCADE,
        related_name="pregnancy_profile",
    )
    gravida = models.PositiveSmallIntegerField(default=1)
    # Gravida: total number of pregnancies (including current).
    para = models.PositiveSmallIntegerField(default=0)
    # Para: number of births after 20 weeks.
    abortions = models.PositiveSmallIntegerField(default=0)
    living_children = models.PositiveSmallIntegerField(default=0)
    last_menstrual_period = models.DateField(null=True, blank=True)
    estimated_delivery_date = models.DateField(null=True, blank=True)
    risk_level = models.CharField(max_length=12, choices=RISK_LEVELS, default="low")
    antenatal_facility = models.CharField(max_length=120, blank=True)
    high_risk_note = models.TextField(blank=True)

    def __str__(self):
        return f"Pregnancy profile — {self.patient}"

    def get_absolute_url(self):        
        return reverse("clinic:patient_detail", args=[self.patient_id])


# ─────────────────────────────────────────────────────────────────────────────
# Clinical note templates
# ─────────────────────────────────────────────────────────────────────────────

class ClinicalNoteTemplate(TimeStampedModel):
    """
    A reusable text template for Routine antenatal visit for example.
    The purpose is to facilitate the clinician note with standards templates.   
    """
    name = models.CharField(max_length=120, unique=True)
    visit_type = models.CharField(max_length=40, default="consultation")
    body = models.TextField()
    # body is the pre-filled text shown in the note form.

    def __str__(self):
        return self.name


# ─────────────────────────────────────────────────────────────────────────────
# Consultation note
# ─────────────────────────────────────────────────────────────────────────────

class ConsultationNote(TimeStampedModel):
    """
    Summary Note after consultation for a single patient visit.
    Many notes can belong to one patient.
    """
    VISIT_TYPES = [
        ("consultation", "Consultation"),
        ("follow_up", "Follow-up"),
        ("antenatal", "Antenatal"),
        ("postnatal", "Postnatal"),
        ("screening", "Screening"),
    ]

    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        related_name="consultations",
    )
    # ForeignKey: many notes can belong to one patient.

    clinician = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="consultation_notes",
    )
    # on_delete=PROTECT: do NOT delete the user if they have consultation notes.

    template = models.ForeignKey(
        ClinicalNoteTemplate,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    # SET_NULL: if the template is deleted, keep the note but set template to NULL.

    consultation_date = models.DateTimeField()
    visit_type = models.CharField(max_length=20, choices=VISIT_TYPES, default="consultation")
    reason_for_visit = models.CharField(max_length=255)
    subjective = models.TextField(blank=True)
    # What the patient reports"
    objective = models.TextField(blank=True)
    # What the clinician observes"
    assessment = models.TextField(blank=True)
    # Clinical conclusion"
    plan = models.TextField(blank=True)
    # Next steps"
    follow_up_date = models.DateField(null=True, blank=True)

    class Meta:
        ordering = ["-consultation_date"]
        # Most recent notes appear first.

    def __str__(self):
        return f"{self.patient} — {self.consultation_date:%Y-%m-%d}"

    def get_absolute_url(self):
        return reverse("clinic:consultationnote_detail", args=[self.pk])


# ─────────────────────────────────────────────────────────────────────────────
# Appointment
# ─────────────────────────────────────────────────────────────────────────────

class Appointment(TimeStampedModel):
    """
    A scheduled visit. Each appointment has a patient, a clinician, a time,
    and a status. 
    """
    STATUS_CHOICES = [
        ("scheduled", "Scheduled"),
        ("done", "Done"),
        ("cancelled", "Cancelled"),
        ("no_show", "No-show"),
    ]

    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        related_name="appointments",
    )
    clinician = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="appointments",
    )
    start_at = models.DateTimeField()
    duration_minutes = models.PositiveSmallIntegerField(default=20)
    purpose = models.CharField(max_length=255)
    location = models.CharField(max_length=120, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="scheduled")
    reminder_sent = models.BooleanField(default=False)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ["start_at"]
        # Nearest appointments appear first.

    def __str__(self):
        return f"{self.patient} — {self.start_at:%Y-%m-%d %H:%M}"

    def get_absolute_url(self):
        return reverse("clinic:appointment_detail", args=[self.pk])


# ─────────────────────────────────────────────────────────────────────────────
# Follow-up reminder
# ─────────────────────────────────────────────────────────────────────────────

class FollowUpReminder(TimeStampedModel):
    """
    A task that reminds the staff to follow up with a patient.
    A reminder becomes "overdue" if its due_date has passed and it is still "pending".
    """
    REMINDER_STATUS = [
        ("pending", "Pending"),
        ("done", "Done"),
        ("overdue", "Overdue"),
    ]

    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        related_name="followups",
    )
    appointment = models.ForeignKey(
        Appointment,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="followups",
    )
    # Optional link to the appointment that triggered the reminder.

    due_date = models.DateField()
    title = models.CharField(max_length=200)
    message = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=REMINDER_STATUS, default="pending")

    class Meta:
        ordering = ["due_date"]
        # Oldest due dates appear first (most urgent at the top).

    def __str__(self):
        return f"{self.patient} — {self.title}"

    def get_absolute_url(self):
        return reverse("clinic:followupreminder_detail", args=[self.pk])