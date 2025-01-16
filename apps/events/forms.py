from django import forms

from .models import Event


class EventForm(forms.ModelForm):
    """Form for creating and updating events."""

    class Meta:
        model = Event
        fields = [
            "title",
            "description",
            "capacity",
            "price",
            "date",
            "status",
            "end_date",
            "hall",
            "image",
        ]
        widgets = {
            "date": forms.DateTimeInput(
                attrs={"class": "form-control", "type": "datetime-local"}
            ),
            "end_date": forms.DateTimeInput(
                attrs={"class": "form-control", "type": "datetime-local"}
            ),
            "description": forms.Textarea(attrs={"class": "form-control"}),
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "capacity": forms.NumberInput(attrs={"class": "form-control"}),
            "price": forms.NumberInput(attrs={"class": "form-control"}),
            "hall": forms.Select(attrs={"class": "form-control"}),
            "image": forms.ClearableFileInput(attrs={"class": "form-control"}),
        }
        read_only_fields = ["seats_available"]
