# forms.py

from django import forms
from django.forms import modelformset_factory

from .models import (
    RecoveryProject,
    ProjectLocations,
    ProjectStatusIndicators,
)

# -------------------------
# Static choices
# -------------------------
SECTOR_CHOICES = [
    ("", "Select sector"),
    ("Health", "Health"),
    ("Education", "Education"),
    ("Infrastructure", "Infrastructure"),
    ("Agriculture", "Agriculture"),
]

FUNDING_STATUS_CHOICES = [
    ("", "Select funding status"),
    ("Planned", "Planned"),
    ("Approved", "Approved"),
    ("Funded", "Funded"),
    ("Ongoing", "Ongoing"),
    ("Completed", "Completed"),
]


# ============================================================
# 1) MAIN FORM: RecoveryProject
# ============================================================
class RecoveryProjectForm(forms.ModelForm):
    sector = forms.ChoiceField(choices=SECTOR_CHOICES, required=False, label="Sector")

    funding_status = forms.ChoiceField(
        choices=FUNDING_STATUS_CHOICES,
        required=False,
        label="Funding status",
    )

    start_date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={"type": "date"}),
        label="Start date",
    )

    completion_date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={"type": "date"}),
        label="Completion date",
    )

    class Meta:
        model = RecoveryProject
        fields = [
            # Project Info
            "sector",
            "program",
            "project_title",
            "project_description",

            # Funding & Dates
            "funding_status",
            "gip",
            "gip_attachment",
            "central_tender_board_link",
            "funding_agency",
            "implementing_agency",
            "project_total_funding_us",
            "project_total_funding_vt",
            "project_expenditure",
            "start_date",
            "completion_date",

            # Risks & Operation Type
            "type_of_disaster_operation",
            "key_risks_to_implementation",
        ]

        widgets = {
            "project_title": forms.Textarea(attrs={"rows": 1}),
            "project_description": forms.Textarea(attrs={"rows": 1}),
            "central_tender_board_link": forms.Textarea(attrs={"rows": 1}),
            "key_risks_to_implementation": forms.Textarea(attrs={"rows": 1}),
            "start_date": forms.DateInput(attrs={"type": "date"}),
            "completion_date": forms.DateInput(attrs={"type": "date"}),
        }

        labels = {
            "gip": "GIP",
            "project_total_funding_us": "Total funding (USD)",
            "project_total_funding_vt": "Total funding (Vatu)",
            "project_expenditure": "Project expenditure",
            "gip_attachment": "GIP Attachment",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            existing = field.widget.attrs.get("class", "")
            field.widget.attrs["class"] = (existing + " form-control").strip()

    def clean(self):
        cleaned_data = super().clean()

        start = cleaned_data.get("start_date")
        end = cleaned_data.get("completion_date")

        if start and end and end >= start:
            cleaned_data["project_timeframe_days"] = (end - start).days
        elif start and end and end < start:
            self.add_error("completion_date", "Completion date cannot be before start date.")

        return cleaned_data


# ============================================================
# 2) SUB-FORM: One ProjectLocations row
# ============================================================
class ProjectLocationForm(forms.ModelForm):
    gps_latitude = forms.DecimalField(
        required=False,
        max_digits=10,
        decimal_places=6,
        widget=forms.TextInput(attrs={
            "placeholder": "e.g. -17.7333",
            "inputmode": "decimal",
        })
    )

    gps_longtitude = forms.DecimalField(
        required=False,
        max_digits=10,
        decimal_places=6,
        widget=forms.TextInput(attrs={
            "placeholder": "e.g. 168.3167",
            "inputmode": "decimal",
        })
    )

    class Meta:
        model = ProjectLocations
        fields = ["province", "island", "area_council", "project_site", "gps_latitude", "gps_longtitude"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            existing = field.widget.attrs.get("class", "")
            field.widget.attrs["class"] = (existing + " form-control").strip()


ProjectLocationFormSet = modelformset_factory(
    ProjectLocations,
    form=ProjectLocationForm,
    extra=1,
    can_delete=True,
)


# ============================================================
# 3) STATUS INDICATORS FORMSET (includes description)
# ============================================================
class ProjectStatusIndicatorForm(forms.ModelForm):
    class Meta:
        model = ProjectStatusIndicators
        fields = ["description"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            existing = field.widget.attrs.get("class", "")
            field.widget.attrs["class"] = (existing + " form-control").strip()


ProjectStatusIndicatorFormSet = modelformset_factory(
    ProjectStatusIndicators,
    form=ProjectStatusIndicatorForm,
    extra=5,
)


from django.forms import BaseModelFormSet, modelformset_factory

class ProjectStatusIndicatorForm(forms.ModelForm):
    class Meta:
        model = ProjectStatusIndicators
        fields = ["description"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            existing = field.widget.attrs.get("class", "")
            field.widget.attrs["class"] = (existing + " form-control").strip()


class BaseProjectStatusIndicatorFormSet(BaseModelFormSet):
    PLACEHOLDERS = [
        "Status Indicator 1",
        "Status Indicator 2",
        "Status Indicator 3",
        "Status Indicator 4",
        "Status Indicator 5",
    ]

    def add_fields(self, form, index):
        super().add_fields(form, index)
        if index is not None and "description" in form.fields:
            ph = self.PLACEHOLDERS[index] if index < len(self.PLACEHOLDERS) else f"Description {index+1}"
            form.fields["description"].widget.attrs["placeholder"] = ph


ProjectStatusIndicatorFormSet = modelformset_factory(
    ProjectStatusIndicators,
    form=ProjectStatusIndicatorForm,
    formset=BaseProjectStatusIndicatorFormSet,
    extra=5,
    can_delete=False,
)


#REGISTRATION
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class RegisterForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            "placeholder": "Enter email address",
            "autocomplete": "email",
        })
    )

    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "password1",
            "password2",
        ]

        widgets = {
            "username": forms.TextInput(attrs={
                "placeholder": "Choose a username",
                "autocomplete": "username",
            }),
        }


#USER EDIT FORM
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import SetPasswordForm


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "first_name",
            "last_name",
            "is_staff",
            "is_superuser",
            "is_active",
        ]

        widgets = {
            "username": forms.TextInput(attrs={
                "class": "form-input",
                "placeholder": "Username",
            }),
            "email": forms.EmailInput(attrs={
                "class": "form-input",
                "placeholder": "Email address",
            }),
            "first_name": forms.TextInput(attrs={
                "class": "form-input",
                "placeholder": "First name",
            }),
            "last_name": forms.TextInput(attrs={
                "class": "form-input",
                "placeholder": "Last name",
            }),
        }

#ADMIN PASSWORD CHANGE
class AdminPasswordChangeForm(SetPasswordForm):
    new_password1 = forms.CharField(
        label="New Password",
        widget=forms.PasswordInput(attrs={
            "class": "form-input",
            "placeholder": "Enter new password",
        })
    )

    new_password2 = forms.CharField(
        label="Confirm New Password",
        widget=forms.PasswordInput(attrs={
            "class": "form-input",
            "placeholder": "Confirm new password",
        })
    )
