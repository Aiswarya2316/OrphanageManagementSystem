from django import forms
from .models import Event

class EventForm(forms.ModelForm):
    event_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'})  # 🗓️ HTML5 Date Picker
    )

    class Meta:
        model = Event
        fields = ['title', 'description', 'event_date', 'children']
