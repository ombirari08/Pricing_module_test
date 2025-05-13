from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import PricingConfig, PricingConfigLog
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
import logging

logger = logging.getLogger(__name__)
# pricing/views.py

from django.shortcuts import render, redirect
from .models import PricingConfig
from .forms import PricingConfigForm  # custom form you'll define

def add_pricing_config(request):
    if request.method == 'POST':
        form = PricingConfigForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('pricing:pricing_calculator_page')
    else:
        form = PricingConfigForm()
    return render(request, 'pricing/add_pricing_config.html', {'form': form})


# API View to calculate the price based on input parameters
@csrf_exempt  # Exempting CSRF for this API endpoint
@api_view(['POST'])
def calculate_price(request):
    try:
        # Parse input
        distance_traveled = float(request.data.get('distance_traveled', 0))
        time_duration = float(request.data.get('time_duration', 0))  # in minutes
        waiting_time = float(request.data.get('waiting_time', 0))  # in minutes
        day_of_week = request.data.get('day_of_week', '').capitalize()

        # Check if day_of_week is valid
        if day_of_week not in dict(PricingConfig.DAYS_OF_WEEK):
            logger.error(f"Invalid day_of_week: {day_of_week}")
            return Response({"error": "Invalid day_of_week."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Check for the active pricing config for the requested day
            config = PricingConfig.objects.get(day_of_week=day_of_week, is_active=True)
        except PricingConfig.DoesNotExist:
            logger.error(f"No active pricing config found for day: {day_of_week}")
            return Response({"error": f"Active pricing configuration not found for the day: {day_of_week}"}, status=status.HTTP_404_NOT_FOUND)

        # Proceed with pricing calculation if config exists
        base_price = float(config.distance_base_price)
        base_km = float(config.distance_base_km)
        additional_km = max(0, distance_traveled - base_km)
        additional_price = additional_km * float(config.distance_additional_price)

        # Time multiplier calculation
        time_multiplier = 1
        for range_str, multiplier in config.time_multiplier_factor.items():
            start, end = map(int, range_str.split('-'))
            if start <= time_duration <= end:
                time_multiplier = multiplier
                break
            elif time_duration > end:
                time_multiplier = multiplier

        # Waiting charges
        waiting_units = max(0, (waiting_time - 3) // 3)
        waiting_total = waiting_units * float(config.waiting_charges)

        # Final price
        total_price = round((base_price + additional_price) * time_multiplier + waiting_total, 2)

        return Response({"total_price": total_price}, status=status.HTTP_200_OK)

    except (ValueError, TypeError) as e:
        logger.error(f"Error processing request: {e}")
        return Response({"error": "Invalid input parameters."}, status=status.HTTP_400_BAD_REQUEST)


# Render the HTML page with the form to calculate the price
def pricing_calculator_page(request):
    # Passing any needed data to the template, e.g., days of the week for the dropdown
    days_of_week = dict(PricingConfig.DAYS_OF_WEEK)  # This assumes PricingConfig.DAYS_OF_WEEK is a tuple of tuples
    return render(request, 'pricing/pricing_calculator.html', {'days_of_week': days_of_week})


# View for modifying an existing pricing configuration
def modify_pricing_config(request, config_id):
    config = get_object_or_404(PricingConfig, id=config_id)

    if request.method == 'POST':
        # Handle form submission to update the config
        config.distance_base_price = request.POST['distance_base_price']
        config.distance_base_km = request.POST['distance_base_km']
        config.distance_additional_price = request.POST['distance_additional_price']
        config.waiting_charges = request.POST['waiting_charges']
        config.time_multiplier_factor = request.POST['time_multiplier_factor']  # Assuming it's a JSON string

        config.save()

        # Log the modification action
        PricingConfigLog.objects.create(
            config=config,
            actor=request.user,
            action='UPDATE'
        )

        return redirect('pricing:pricing_calculator_page')  # Redirect back to the pricing calculator page

    return render(request, 'pricing/modify_pricing_config.html', {'config': config})


# View for deleting an existing pricing configuration
def delete_pricing_config(request, config_id):
    config = get_object_or_404(PricingConfig, id=config_id)

    if request.method == 'POST':
        # Log the delete action
        PricingConfigLog.objects.create(
            config=config,
            actor=request.user,
            action='DELETE'
        )

        config.delete()
        return redirect('pricing:pricing_calculator_page')  # Redirect back to the pricing calculator page

    return render(request, 'pricing/delete_pricing_config.html', {'config': config})
