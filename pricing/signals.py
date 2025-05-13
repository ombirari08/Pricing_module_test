from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import PricingConfig, PricingConfigLog
from django.contrib.auth.models import User

@receiver(post_save, sender=PricingConfig)
def log_pricing_update(sender, instance, created, **kwargs):
    # Actor info should be ideally passed from request; for admin panel, we can override admin save_model to pass actor
    pass  # Will implement logging in admin override to capture actor

@receiver(post_delete, sender=PricingConfig)
def log_pricing_delete(sender, instance, **kwargs):
    # Similar implementation to log deletion
    pass
