from django import forms
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.contrib.auth.models import User, Group

from .models import(
    Patient,
    StaffProfile,
    MedicalHistory,
    PregnancyProfile,
    Appointment,
    ClinicalNoteTemplate,
    ConsultationNote,
    FollowUpReminder,    
)


# ----------------------------------------------------------------------------
# DaisyUI form mixin : To add DaisyUI CSS classes to every field in a form
# ----------------------------------------------------------------------------

class DaisyFormMixin:
    input_class    = "input input-bordered w-full"
    textarea_class = "textarea textarea-bordered w-full"
    select_class   = "select select-bordered w-full"
    checkbox_class = "checkbox"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            widget = field.widget
            if isinstance(widget, forms.CheckboxInput):
                widget.attrs["class"] = self.checkbox_class
            elif isinstance(widget, forms.Textarea):
                widget.attrs["class"] = self.textarea_class            
            elif isinstance(widget, (forms.Select, forms.SelectMultiple)):
                widget.attrs["class"] = self.select_class
            else:
                widget.attrs["class"] = self.input_class


# ----------------------------------------------------------------------------
# Patient Management forms
# ----------------------------------------------------------------------------

# Patient forms

class PatientForm(DaisyFormMixin, forms.ModelChoiceIterator):
    class Meta:
        model = Patient
        fields = [
            "first_name", "last_name","sex", "date_of_birth", "phone", "email", "region", "city", 
            "address", "occupation", "emergency_contact_name", "notes", "is_active",
        ]
        
        widgets = {
            "date_of_birth":    forms.DateInput(attrs={"type": "date"}),
            "notes":            forms.Textarea(attrs={"rows": 4}),
        }
      

# MedicalHistory forms

class MedicalHistoryForm(DaisyFormMixin, forms.ModelForm):
 class Meta:
     model = MedicalHistory
     fields = [
         "blood_group", "hypertension", "diabetes", "sickle_cell_disease", "hiv_positive", "tuberculosis", "hepatitis_b",
         "epilepsy", "asthma", "other_chronic", "previous_surgeries", "allergies", "current_medications", "family_history",
         "smoking", "alcohol", "additional_notes",
     ]

     widgets = {
         "other_chronic":       forms.Textarea(attrs={"rows": 3}),
         "previous_surgeries":  forms.Textarea(attrs={"rows": 3}),
         "allergies":           forms.Textarea(attrs={"rows": 3}),
         "current_medications": forms.Textarea(attrs={"rows": 3}),
         "family_history":      forms.Textarea(attrs={"rows": 3}),
         "additional_notes":    forms.Textarea(attrs={"rows": 3}),
     }


# PregnancyProfile forms

class PregnancyProfileForm(DaisyFormMixin, forms.ModelForm):
    class Meta:
        model = PregnancyProfile
        fields = [
            "gravida", "para", "abortions", "living_children", "last_menstrual_period",
            "estimated_delivery_date", "risk_level", "antenatal_facility", "high_risk_note"
        ]

        widgets = {
            "last_menstrual_period":    forms.DateInput(attrs={"type": "date"}),
            "estimated_delivery_date":  forms.DateInput(attrs={"type": "date"}),
            "high_risk_note":           forms.Textarea(attrs={"rows": 4}),
        }


# Appointment forms

class AppointmentForm(DaisyFormMixin, forms.ModelForm):
    class Meta:
        model = Appointment
        fields = [
            "patient", "clinician", "start_at", "duration_minutes",
            "purpose", "location", "status", "reminder_sent", "notes",
        ]

        widgets = {
            "start_at": forms.DateTimeInput(attrs={"type": "datetime-local"}),
            "notes":    forms.Textarea(attrs={"rows": 4}),
        }


# ClinicalNoteTemplate forms

class ClinicalNoteTemplateForm(DaisyFormMixin, forms.ModelForm):
    class Meta:
        model = ClinicalNoteTemplate
        fields = [
            "name", "visit_type", "body"
        ]

        widgets = {
            "body": forms.Textarea(attrs={"rows": 10})
        }


# ConsultationNote forms

class ConsultationNoteForm(DaisyFormMixin, forms.ModelForm):
    class Meta:
        model = ConsultationNote
        fields = [
            "patient", "clinician", "template", "consultation_date", "visit_type", "reason_for_visit",
            "subjective", "objective", "assessment", "plan", "follow_up_date"
        ]

        widgets = {
            "consultation_date":    forms.Textarea(attrs={"rows": 3}),
            "subjective":           forms.Textarea(attrs={"rows": 3}),
            "objective":            forms.Textarea(attrs={"rows": 3}),
            "assessment":           forms.Textarea(attrs={"rows": 3}),
            "plan":                 forms.Textarea(attrs={"rows": 4}),
            "follow_up_date":       forms.DateInput(attrs={"type": "date"}),
        }


# FollowUpReminder forms

class FollowUpReminderForm(DaisyFormMixin, forms.ModelForm):
    class Meta:
        model = FollowUpReminder
        fields = [
            "patient", "appointment", "due_date", "title", "message", "status",
        ]

        widgets = {           
            "due_date": forms.DateInput(attrs={"type": "date"}),
            "messate":  forms.Textarea(attrs={"rows": 4}),
        }


# ----------------------------------------------------------------------------
# User Management forms
# ----------------------------------------------------------------------------

# Staff User Creation form

class StaffUserCreationForm(DaisyFormMixin, UserCreationForm):
  groups = forms.ModelMultipleChoiceField(
      queryset = Group.objects.all(),
      required = False,
      widget = forms.CheckboxSelectMultiple,
      help_text = "Select one or more roles for this specific user.",
  )

  class meta:
      model = User
      fields = [
          "username", "first_name", "last_name", "email",
          "is_staff", "is_active", "groups",
      ]


# Staff User Update form

class StaffUserUpdateForm(DaisyFormMixin, UserChangeForm):
    password = None
    groups = forms.ModelMultipleChoiceField(
        queryset = Group.objects.all(),
        required = False,
        widget = forms.CheckboxSelectMultiple,
        help_text = "Update one or more roles for this specific user.",
    )

    class Meta:
        model = User
        fields = [            
            "username", "first_name", "last_name", "email",
            "is_staff", "is_active", "groups",
        ]


# Staff Profile form

class StaffProfileForm(DaisyFormMixin, forms.ModelForm):
  
  class Meta:
      model = StaffProfile
      fields = [
          "role_label", "phone", "bio", "avatar_url"
      ]

      widgets = {
          "bio": forms.Textarea(attrs={"rows": 4}),
      }
  


 

 
    
   
     
  StaffProfile,