from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError


class PricingConfig(models.Model):
    DAYS_OF_WEEK = [
    ('Monday', 'Monday'),
    ('Tuesday', 'Tuesday'),
    ('Wednesday', 'Wednesday'),
    ('Thursday', 'Thursday'),
    ('Friday', 'Friday'),
    ('Saturday', 'Saturday'),
    ('Sunday', 'Sunday'),
]


    day_of_week = models.CharField(
        max_length=10,
        choices=DAYS_OF_WEEK,
        help_text="Applicable day of the week for this pricing config"
    )

    distance_base_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        help_text="Base price for distance up to distance_base_km"
    )

    distance_base_km = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        help_text="Base kilometers covered in base price"
    )

    distance_additional_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        help_text="Rate per km after base distance"
    )

    time_multiplier_factor = models.JSONField(
        help_text="Time-based multiplier (e.g. {'0-60': 1, '61-120': 1.25, '121-180': 2.2})"
    )

    waiting_charges = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        help_text="Charge per 3 mins after initial 3 mins wait"
    )

    is_active = models.BooleanField(
        default=True,
        help_text="Only one active config per day is used"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def clean(self):
        if self.is_active:
            conflict = PricingConfig.objects.filter(
                day_of_week=self.day_of_week,
                is_active=True
            ).exclude(pk=self.pk)
            if conflict.exists():
                raise ValidationError(
                    f"Another active config already exists for {self.get_day_of_week_display()}."
                )

    def save(self, *args, **kwargs):
        self.full_clean()  # trigger clean() before saving
        super().save(*args, **kwargs)

    def __str__(self):
        return f"[{self.get_day_of_week_display()}] Base ₹{self.distance_base_price} ({self.distance_base_km}KM) | Active: {self.is_active}"


from django.db import models
from django.contrib.auth.models import User


class PricingConfigLog(models.Model):
    ACTION_CHOICES = [
        ('CREATE', 'Create'),
        ('UPDATE', 'Update'),
        ('DELETE', 'Delete'),
    ]

    # ForeignKey to PricingConfig
    config = models.ForeignKey(
        'PricingConfig',  # You can use a string for the model name to avoid circular imports
        on_delete=models.CASCADE,
        related_name='pricing_config_logs',
        help_text="The pricing config that was changed"
    )

    # ForeignKey to User, indicating who made the change
    actor = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,  # Allow blank if actor is not always available (like 'system')
        help_text="User who made the change"
    )

    # Action performed (CREATE, UPDATE, DELETE)
    action = models.CharField(
        max_length=6,
        choices=ACTION_CHOICES,
        help_text="What action was performed on the pricing config"
    )

    # Timestamp of when the action occurred
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.get_action_display()} on {self.config} by {self.actor if self.actor else 'System'} at {self.timestamp:%Y-%m-%d %H:%M:%S}"






