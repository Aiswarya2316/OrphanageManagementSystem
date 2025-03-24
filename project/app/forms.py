from django import forms
from .models import Event

class EventForm(forms.ModelForm):
    event_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        input_formats=['%Y-%m-%d']  # ✅ Ensures correct format
    )

    class Meta:
        model = Event
        fields = ['title', 'description', 'event_date', 'conducted_by', 'image']
