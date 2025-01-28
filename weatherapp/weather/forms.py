from django import forms
from .models import WeatherSearch

class WeatherSearchUpdateForm(forms.ModelForm):
    class Meta:
        model = WeatherSearch
        fields = ['temperature', 'weather_description', 'weather_icon', 'wind_speed', 'humidity']
        widgets = {
            'weather_description': forms.Textarea(attrs={'rows': 3, 'cols': 40}),
        }
