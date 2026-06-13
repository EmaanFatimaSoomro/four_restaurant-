from django.conf import settings


def restaurant_settings(request):
    """Inject restaurant-wide settings into every template context."""
    return {
        'RESTAURANT_NAME':    settings.RESTAURANT_NAME,
        'RESTAURANT_TAGLINE': settings.RESTAURANT_TAGLINE,
        'RESTAURANT_ADDRESS': settings.RESTAURANT_ADDRESS,
        'RESTAURANT_PHONE':   settings.RESTAURANT_PHONE,
        'RESTAURANT_EMAIL':   settings.RESTAURANT_EMAIL,
        'RESTAURANT_HOURS':   settings.RESTAURANT_HOURS,
    }
