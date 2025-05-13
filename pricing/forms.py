from django import forms
from .models import PricingConfig
from django.core.exceptions import ValidationError

class PricingConfigForm(forms.ModelForm):
    class Meta:
        model = PricingConfig
        fields = [
            'day_of_week',
            'distance_base_price',
            'distance_base_km',
            'distance_additional_price',
            'time_multiplier_factor',
            'waiting_charges',
            'is_active'
        ]
        widgets = {
            'time_multiplier_factor': forms.Textarea(attrs={
                'rows': 3,
                'cols': 30,
                'class': 'form-control',
                'placeholder': 'e.g. {"0-10": 1.0, "11-30": 1.5, "31-60": 2.0}'
            }),
        }

    def __init__(self, *args, **kwargs):
        super(PricingConfigForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name == 'time_multiplier_factor':
                continue  # Already styled in widgets
            if isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs.update({'class': 'form-check-input'})
            elif isinstance(field.widget, forms.Select):
                field.widget.attrs.update({'class': 'form-select'})
            else:
                field.widget.attrs.update({'class': 'form-control'})

    def clean(self):
        cleaned_data = super().clean()
        day_of_week = cleaned_data.get('day_of_week')
        is_active = cleaned_data.get('is_active')

        # Check for conflicts with active configurations for the same day
        if is_active:
            conflict = PricingConfig.objects.filter(
                day_of_week=day_of_week, is_active=True
            ).exclude(pk=self.instance.pk)
            if conflict.exists():
                raise ValidationError(f"Another active pricing config already exists for {day_of_week}.")

        return cleaned_data
