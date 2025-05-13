# pricing/urls.py

from django.urls import path
from . import views

app_name = 'pricing'

urlpatterns = [
    path('', views.add_pricing_config, name='add_pricing_config'),  # ROOT points to add form
    path('pricing-calculator/', views.pricing_calculator_page, name='pricing_calculator_page'),
    path('api/calculate-price/', views.calculate_price, name='calculate_price'),
    path('modify-pricing-config/<int:config_id>/', views.modify_pricing_config, name='modify_pricing_config'),
    path('delete-pricing-config/<int:config_id>/', views.delete_pricing_config, name='delete_pricing_config'),
]
