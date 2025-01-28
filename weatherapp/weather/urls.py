from django.urls import path

from . import views


urlpatterns = [
    path('', views.weather_view, name='weather'),
    path('list/', views.weather_list, name='weather_list'),
    path('delete/<int:search_id>/', views.delete_weather_search, name='delete_weather_search'),
    path('update/<int:search_id>/', views.update_weather_search, name='update_weather_search'),
    path('add_to_history/', views.add_to_history, name='add_to_history'),
]