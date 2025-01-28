from django.db import models
from django.conf import settings

class WeatherSearch(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    city = models.CharField(max_length=255)
    temperature = models.FloatField()
    weather_description = models.CharField(max_length=255)
    weather_icon = models.URLField()  # URL to the weather icon image
    wind_speed = models.FloatField()
    humidity = models.FloatField()
    date_searched = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Weather search for {self.city} by {self.user.username}"

    class Meta:
        ordering = ['-date_searched']  # To display the most recent searches first
