from django.contrib import admin
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

# Register your models here.

@admin.register(StaffProfile)
class StaffProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "role_label", "phone")
    list_filter = ("role_label", "user")
    search_fields = ("user__username", "user__first_name", "user__last_name")


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ("last_name", "first_name", "city", "phone", "is_active")
    list_filter = ("city", "is_active")
    search_fields = ("first_name", "last_name", "phone", "city")


@admin.register(MedicalHistory)
class MedicalHistoryAdmin(admin.ModelAdmin):
    list_display = ("patient", "medications", "chronic_conditions", "allergies", "past_surgeries")
    list_filter = ("patient", "allergies")


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ("patient", "clinician", "start_at", "status", "reminder_sent")
    list_filter = ("status", "clinician")


@admin.register(PregnancyProfile)
class PregnancyProfileAdmin(admin.ModelAdmin):
    list_display = ("patient", "gravida", "para", "risk_level", "estimated_delivery_date")
    list_filter = ("risk_level", "patient")


@admin.register(ConsultationNote)
class ConsultationNoteAdmin(admin.ModelAdmin):
    list_display = ("patient", "clinician", "visit_type", "consultation_date", "follow_up_date")
    list_filter = ("visit_type", "clinician")
    search_fields = ("patient__first_name", "patient__last_name")


@admin.register(ClinicalNoteTemplate)
class ClinicalNoteTemplateAdmin(admin.ModelAdmin):
    list_display = ("name", "visit_type", "created_at")
    search_fields = ("name", "visit_type")


@admin.register(FollowUpReminder)
class FollowUpReminderAdmin(admin.ModelAdmin):
    list_display = ("patient", "title", "due_date", "status")
    list_filter = ("status", "due_date")