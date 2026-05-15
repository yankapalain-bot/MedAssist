import random
from datetime import timedelta

from django.contrib.auth.models import Group, User
from django.core.management.base import BaseCommand
from django.utils import timezone
from faker import Faker

from clinic.models import (
    Patient,
    StaffProfile,
    MedicalHistory,
    PregnancyProfile,
    Appointment,
    ClinicalNoteTemplate,
    ConsultationNote,
    FollowUpReminder,    
    
)

fake = Faker()

# ── Patients (Womens) ────────────────────────────────────────────────

FEMALE_FIRST_NAMES = [
    "Amina", "Fatima", "Nadia", "Viviane", "Sylvie", "Christelle",
    "Marie-Claire", "Hortense", "Jacqueline", "Solange", "Eugénie",
    "Danielle", "Pauline", "Sandrine", "Florence", "Aïcha", "Ramatou",
    "Marthe", "Cécile", "Thérèse", "Véronique", "Agnès", "Blandine",
    "Immaculée", "Rose", "Séraphine", "Honorine", "Léontine", "Edwige",
    "Philomène", "Nathalie", "Isabelle", "Brigitte", "Jeanne", "Bernadette",
    "Lucie", "Angèle", "Yvette", "Monique", "Georgette",
]

LAST_NAMES = [
    "Ngo Biyong", "Mbarga", "Tchouakeu", "Ndongo", "Essomba", "Mbassi",
    "Mvondo", "Ngono", "Etoga", "Abomo", "Atangana", "Beti",
    "Djomo", "Feudjio", "Fomekong", "Guifo", "Kamga", "Kwekam",
    "Lekene", "Meka", "Nana", "Nfon", "Nkeng", "Onana",
    "Ondoa", "Simo", "Talla", "Tchatchoua", "Tchinda", "Wamba",
    "Nguenang", "Noubissi", "Pouokam", "Temdie", "Tsamo", "Youmbi",
    "Djoumessi", "Fopah", "Gankoue", "Happi",
]

CITIES = [
    "Yaoundé", "Douala", "Bamenda", "Bafoussam",
    "Garoua", "Maroua", "Bertoua", "Ebolowa",
]

REGIONS = {
    "Yaoundé": "Centre",
    "Douala": "Littoral",
    "Bamenda": "North West",
    "Bafoussam": "West",
    "Garoua": "North",
    "Maroua": "Far North",
    "Bertoua": "East",
    "Ebolowa": "South",
}

OCCUPATIONS = [
    "Teacher", "Nurse", "Merchant", "Farmer", "Civil servant",
    "Seamstress", "Hairdresser", "Student", "Housewife", "Accountant",
    "Secretary", "Midwife", "Social worker", "Pharmacist", "Cook",
]

VISIT_REASONS = [
    "Routine antenatal visit",
    "Pregnancy confirmation",
    "High blood pressure follow-up",
    "Gestational diabetes check",
    "Pelvic pain consultation",
    "Ultrasound follow-up review",
    "Post-natal check-up",
    "Contraceptive counselling",
    "Cervical cancer screening",
    "Irregular menstrual cycles",
    "Iron deficiency anaemia",
    "Urinary tract infection",
    "Vaginal discharge evaluation",
    "Pre-conception counselling",
    "Menopause consultation",
]

NOTE_TEMPLATES_DATA = [
    {
        "name": "Routine antenatal visit",
        "visit_type": "antenatal",
        "body": (
            "SUBJECTIVE: Patient attends for routine antenatal visit. "
            "No significant complaints. Baby moving well.\n\n"
            "OBJECTIVE: BP ___, Weight ___ kg, FHR ___ bpm, Fundal height ___ cm.\n\n"
            "ASSESSMENT: ___ weeks gestation. Uncomplicated pregnancy.\n\n"
            "PLAN: Continue iron and folic acid. Next visit in 4 weeks. "
            "Return earlier if reduced foetal movement, bleeding, or severe headache."
        ),
    },
    {
        "name": "High-risk antenatal — hypertension",
        "visit_type": "antenatal",
        "body": (
            "SUBJECTIVE: Patient presents with raised blood pressure at home. "
            "Headaches: ___. Visual disturbance: ___. Oedema: ___.\n\n"
            "OBJECTIVE: BP ___, Weight ___, Urinalysis: protein ___. FHR ___.\n\n"
            "ASSESSMENT: Pre-eclampsia / gestational hypertension at ___ weeks.\n\n"
            "PLAN: Antihypertensive therapy. Foetal monitoring. "
            "Hospital admission if BP >160/110 or proteinuria 3+."
        ),
    },
    {
        "name": "Post-natal 6-week check",
        "visit_type": "postnatal",
        "body": (
            "SUBJECTIVE: Patient returns at 6 weeks post delivery. "
            "Breastfeeding: ___. Mood: ___. Wound healing: ___.\n\n"
            "OBJECTIVE: Weight ___, BP ___, Uterus involution: ___.\n\n"
            "ASSESSMENT: Post-natal recovery ___.\n\n"
            "PLAN: Contraceptive counselling completed. Family planning method: ___. "
            "Return if concerns."
        ),
    },
    {
        "name": "Gynaecology consultation",
        "visit_type": "consultation",
        "body": (
            "SUBJECTIVE: Patient presents with ___.\n\n"
            "OBJECTIVE: Abdomen: ___. Pelvic exam: ___.\n\n"
            "ASSESSMENT: ___.\n\n"
            "PLAN: ___. Follow-up in ___ weeks."
        ),
    },
]


class Command(BaseCommand):
    help = "Seed the database with realistic gynecology clinic demo data."

    def add_arguments(self, parser):
        parser.add_argument(
            "--clear",
            action="store_true",
            help="Clear all existing demo data before seeding.",
        )

    def handle(self, *args, **options):
        if options["clear"]:
            self.stdout.write("Clearing existing data…")
            FollowUpReminder.objects.all().delete()
            Appointment.objects.all().delete()
            ConsultationNote.objects.all().delete()
            PregnancyProfile.objects.all().delete()
            MedicalHistory.objects.all().delete()
            Patient.objects.all().delete()
            ClinicalNoteTemplate.objects.all().delete()
            StaffProfile.objects.all().delete()
            User.objects.filter(is_superuser=False).delete()
            self.stdout.write(self.style.WARNING("Cleared."))

        # ── Groups ────────────────────────────────────────────────────────────
        clinician_group, _ = Group.objects.get_or_create(name="Clinicians")
        reception_group, _ = Group.objects.get_or_create(name="Reception")
        manager_group, _   = Group.objects.get_or_create(name="Managers")

        # ── Staff users ───────────────────────────────────────────────────────
        staff_data = [
            ("dr.ngono",      "Marie",    "Ngono",    "clinician", clinician_group),
            ("dr.mvondo",     "Boris",     "Toghuem",   "clinician", clinician_group),
            ("reception.amina","Amina",   "Bello",    "reception", reception_group),
            ("mgr.henang",      "Patrick", "Henang",     "manager",   manager_group),
        ]
        staff_users = []
        for username, first, last, role, group in staff_data:
            user, created = User.objects.get_or_create(
                username=username,
                defaults={
                    "first_name": first,
                    "last_name":  last,
                    "email": f"{username}@medassist.cm",
                    "is_staff": True,
                    "is_active": True,
                },
            )
            if created:
                user.set_password("medassist2025")
                user.save()
                user.groups.add(group)
                StaffProfile.objects.create(user=user, role_label=role, phone=f"+237 6{random.randint(10,99)} {random.randint(100,999)} {random.randint(100,999)}")
                self.stdout.write(f"  Created user: {username}")
            staff_users.append(user)

        # Get clinicians for linking to consultations and appointments
        clinicians = list(User.objects.filter(groups=clinician_group))
        if not clinicians:
            clinicians = staff_users[:1]

        # ── Note templates ────────────────────────────────────────────────────
        for tpl in NOTE_TEMPLATES_DATA:
            ClinicalNoteTemplate.objects.get_or_create(
                name=tpl["name"],
                defaults={"visit_type": tpl["visit_type"], "body": tpl["body"]},
            )
        self.stdout.write(f"  Templates: {ClinicalNoteTemplate.objects.count()}")

        # ── Patients ───────────────────────────────────────────────
        now = timezone.now()
        patients = []
        for i in range(60):
            city = random.choice(CITIES)
            fname = random.choice(FEMALE_FIRST_NAMES)
            lname = random.choice(LAST_NAMES)
            age_days = random.randint(15 * 365, 50 * 365)
            patient = Patient.objects.create(
                first_name=fname,
                last_name=lname,
                sex="F",
                date_of_birth=(now - timedelta(days=age_days)).date(),
                phone=f"+237 6{random.randint(50,79)} {random.randint(100,999)} {random.randint(100,999)}",
                email=f"{fname.lower().replace(' ','.')}.{lname.lower().split()[0]}@gmail.com"
                      if random.random() > 0.5 else "",
                city=city,
                region=REGIONS[city],
                address=f"Quartier {random.choice(['Melen','Bastos','Nlongkak','Essos','Nkol-Eton','Mvog-Ada','Elig-Essono'])}",
                occupation=random.choice(OCCUPATIONS),
                emergency_contact_name=f"{random.choice(FEMALE_FIRST_NAMES)} {random.choice(LAST_NAMES)}",
                emergency_contact_phone=f"+237 6{random.randint(50,79)} {random.randint(100,999)} {random.randint(100,999)}",
                is_active=random.random() > 0.08,
            )
            patients.append(patient)

        self.stdout.write(f"  Patients: {Patient.objects.count()}")

        # ── Medical history (for all patients) ────────────────────
        for patient in patients:
            MedicalHistory.objects.create(
               patient=patient,
               allergies=fake.sentence(),
               chronic_conditions=fake.sentence(),
               medications=fake.sentence(),
               past_surgeries=fake.sentence(),
            )
            
        self.stdout.write(f"  Medical History: {MedicalHistory.objects.count()}")

        # ── Pregnancy profiles (for 40 of the 60 patients) ────────────────────
        for patient in random.sample(patients, k=40):
            gravida = random.randint(1, 5)
            lmp_days_ago = random.randint(60, 260)
            lmp = (now - timedelta(days=lmp_days_ago)).date()
            edd = lmp + timedelta(days=280)
            PregnancyProfile.objects.create(
                patient=patient,
                gravida=gravida,
                para=max(0, gravida - 1),
                abortions=random.randint(0, 2),
                living_children=max(0, gravida - 1),
                last_menstrual_period=lmp,
                estimated_delivery_date=edd,
                risk_level=random.choices(
                    ["low", "moderate", "high"],
                    weights=[60, 30, 10]
                )[0],
                antenatal_facility=f"Centre de Santé {random.choice(['Nlongkak','Bastos','Mvog-Mbi','Biyem-Assi'])}",
            )

        self.stdout.write(f"  Pregnancy profiles: {PregnancyProfile.objects.count()}")

        # ── Consultation notes ────────────────────────────────────────────────
        templates = list(ClinicalNoteTemplate.objects.all())
        visit_types = ["consultation", "follow_up", "antenatal", "postnatal", "screening"]

        for patient in patients:
            n_notes = random.randint(1, 5)
            for j in range(n_notes):
                days_ago = random.randint(1, 365)
                vtype = random.choice(visit_types)
                tpl = random.choice(templates) if templates else None
                ConsultationNote.objects.create(
                    patient=patient,
                    clinician=random.choice(clinicians),
                    template=tpl,
                    consultation_date=now - timedelta(days=days_ago),
                    visit_type=vtype,
                    reason_for_visit=random.choice(VISIT_REASONS),
                    subjective=f"Patient reports {random.choice(['mild discomfort','no significant complaints','occasional headaches','fatigue','nausea'])}.",
                    objective=f"BP {random.randint(100,140)}/{random.randint(60,90)}. Weight {random.randint(45,90)} kg.",
                    assessment=random.choice([
                        "Normal findings for gestational age.",
                        "Mild anaemia. Iron supplementation advised.",
                        "Well-controlled hypertension.",
                        "No acute pathology identified.",
                        "Gestational diabetes — dietary management ongoing.",
                    ]),
                    plan=random.choice([
                        "Continue current medications. Review in 4 weeks.",
                        "Repeat blood tests in 2 weeks.",
                        "Refer to specialist.",
                        "Discharge with advice. Return if symptoms worsen.",
                        "Increase iron supplementation. High-protein diet advised.",
                    ]),
                    follow_up_date=(now + timedelta(days=random.randint(7, 60))).date()
                               if random.random() > 0.4 else None,
                )

        self.stdout.write(f"  Consultation notes: {ConsultationNote.objects.count()}")

        # ── Appointments ──────────────────────────────────────────────────────
        status_choices = ["scheduled", "done", "cancelled", "no_show"]
        status_weights = [40, 40, 10, 10]
        purposes = [
            "Antenatal visit", "Follow-up consultation", "Postnatal check",
            "Screening", "Blood test review", "Ultrasound review",
        ]
        for patient in patients:
            n_appts = random.randint(1, 4)
            for _ in range(n_appts):
                offset = random.randint(-30, 30)
                appt_time = now + timedelta(days=offset, hours=random.randint(7, 16))
                status = random.choices(status_choices, weights=status_weights)[0]
                if offset > 0:
                    status = "scheduled"
                elif offset < -7:
                    status = random.choice(["done", "no_show", "cancelled"])
                Appointment.objects.create(
                    patient=patient,
                    clinician=random.choice(clinicians),
                    start_at=appt_time,
                    duration_minutes=random.choice([15, 20, 30]),
                    purpose=random.choice(purposes),
                    location="Consultation Room " + str(random.randint(1, 4)),
                    status=status,
                )

        self.stdout.write(f"  Appointments: {Appointment.objects.count()}")

        # ── Follow-up reminders ───────────────────────────────────────────────
        reminder_titles = [
            "Repeat blood pressure check",
            "Blood glucose follow-up",
            "Haemoglobin recheck",
            "Return if labour signs",
            "Contraception review",
            "Referral follow-up",
            "Medication compliance check",
        ]
        statuses = ["pending", "done", "overdue"]
        status_weights_rem = [50, 30, 20]

        for patient in random.sample(patients, k=45):
            for _ in range(random.randint(1, 3)):
                due_offset = random.randint(-10, 30)
                due = (now + timedelta(days=due_offset)).date()
                status = random.choices(statuses, weights=status_weights_rem)[0]
                if due_offset < 0 and status == "pending":
                    status = "overdue"
                FollowUpReminder.objects.create(
                    patient=patient,
                    due_date=due,
                    title=random.choice(reminder_titles),
                    message=f"Please ensure {patient.first_name} returns for this follow-up.",
                    status=status,
                )

        self.stdout.write(f"  Reminders: {FollowUpReminder.objects.count()}")
        self.stdout.write(self.style.SUCCESS("\n✅ Seed complete! Login: dr.ngono / medassist2025"))