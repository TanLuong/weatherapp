from datetime import datetime
import traceback

import requests
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import WeatherSearch
from .forms import WeatherSearchUpdateForm
from django.core.paginator import Paginator
from django.http import JsonResponse


def weather_view(request):
    # Get the city from the user input (default to a city if not entered)
    client_ip = request.META.get('REMOTE_ADDR')
    try:
        url = f'https://ipinfo.io/{client_ip}/city'
        response = requests.get(url)
        # Parse the response JSON
        if response.status_code != 200:
            city = request.GET.get('city', 'New York')
        else:
            city = request.GET.get('city', response.text.strip())
        # Weatherstack API URL
        url = f'{settings.API_URL}/current?access_key={settings.WEATHERSTACK_API_KEY}&query={city}'
        response = requests.get(url)
        data = response.json()
        if 'error' in data:
            return render(request, 'weather/error.html', {
                'message': data['error']['info'],
            })
        
        weather_current = data['current']
        
        return render(request, 'weather/weather.html', {
            'user': request.user,
            'weather': weather_current,
            'current_date': datetime.now(),
            'location': data['location']['name'],
        })
    except Exception as e:
        traceback.print_exc()
        return render(request, 'weather/error.html', {
                'message': "Something went wrong. Please try again later",
    })


def weather_view(request):
    # Get the city from the user input (default to a city if not entered)
    client_ip = request.META.get('REMOTE_ADDR')
    try:
        url = f'https://ipinfo.io/{client_ip}/city'
        response = requests.get(url)
        # Parse the response JSON
        if response.status_code != 200:
            city = request.GET.get('city', 'New York')
        else:
            city = request.GET.get('city', response.text.strip())
        # Weatherstack API URL
        url = f'{settings.API_URL}/current?access_key={settings.WEATHERSTACK_API_KEY}&query={city}'
        response = requests.get(url)
        data = response.json()
        if 'error' in data:
            return render(request, 'weather/error.html', {
                'message': data['error']['info'],
            })
        
        weather_current = data['current']
        
        return render(request, 'weather/weather.html', {
            'user': request.user,
            'weather': weather_current,
            'current_date': datetime.now(),
            'location': data['location']['name'],
        })
    except Exception as e:
        traceback.print_exc()
        return render(request, 'weather/error.html', {
                'message': "Something went wrong. Please try again later",
    })

@login_required
def add_to_history(request):
    if request.method == 'POST':
        # Extract weather data from the request (you can pass it via JavaScript or form data)
        location = request.POST.get('location')
        temperature = request.POST.get('temperature')
        humidity = request.POST.get('humidity')
        wind_speed = request.POST.get('wind_speed')
        weather_icon = request.POST.get('weather_icon')
        feels_like = request.POST.get('feels_like')
        weather_descriptions = request.POST.get('weather_descriptions')
        try:
        # Create a new WeatherHistory record
            w1 = WeatherSearch.objects.create(
                user=request.user,
                city=location,
                temperature=temperature,
                humidity=humidity,
                wind_speed=wind_speed,
                weather_icon=weather_icon,
                weather_description=weather_descriptions,
            )
            message = 'record added successfully'
        except Exception as e:
            traceback.print_exc()
            message = 'Failed to add record'
        finally:
            return JsonResponse({'message': message})


# View for listing all saved weather searches with pagination
@login_required
def weather_list(request):
    weather_searches = WeatherSearch.objects.filter(user=request.user)
    paginator = Paginator(weather_searches, 5)  # Show 5 records per page
    page_number = request.GET.get('page', 1)
    page_obj = paginator.page(page_number)

    return render(request, 'weather/weather_list.html', {
        'page_obj': page_obj,
    })

# View for deleting a weather search
@login_required
def delete_weather_search(request, search_id):
    try:
        weather_search = WeatherSearch.objects.get(id=search_id, user=request.user)
        weather_search.delete()
        messages.success(request, "Weather search deleted successfully!")
    except WeatherSearch.DoesNotExist:
        messages.error(request, "Weather search not found.")
    
    return redirect('weather_list')  # Redirect back to the list page

# View for updating a weather search
@login_required
def update_weather_search(request, search_id):
    weather_search = get_object_or_404(WeatherSearch, id=search_id, user=request.user)
    
    if request.method == 'POST':
        form = WeatherSearchUpdateForm(request.POST, instance=weather_search)
        if form.is_valid():
            form.save()
            messages.success(request, "Weather search updated successfully!")
            return redirect('weather_list')
    else:
        form = WeatherSearchUpdateForm(instance=weather_search)

    return render(request, 'weather/weather_update.html', {'form': form, 'weather_search': weather_search})
