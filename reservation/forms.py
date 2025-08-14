from django import forms
from .models import Reservation

from .models import Feedback


class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ["name", "email", "message"]


class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = [
            "table",
            "reservation_time",
            "number_of_guests",
            "customer_name",
            "customer_phone",
        ]
        widgets = {
            "reservation_time": forms.DateTimeInput(
                attrs={"type": "datetime-local", "class": "form-control"},
                format="%Y-%m-%dT%H:%M",
            ),
            "number_of_guests": forms.NumberInput(attrs={"class": "form-control"}),
            "customer_name": forms.TextInput(attrs={"class": "form-control"}),
            "customer_phone": forms.TextInput(attrs={"class": "form-control"}),
            "table": forms.Select(attrs={"class": "form-control"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["reservation_time"].input_formats = ["%Y-%m-%dT%H:%M"]
