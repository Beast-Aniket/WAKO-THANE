from django.utils import timezone

from core.models import SiteSettings


def site_settings(request):
    return {
        "site_settings": {
            "hero_title": SiteSettings.get("hero_title", "Train hard. Fight smart. Represent Thane."),
            "hero_subtitle": SiteSettings.get(
                "hero_subtitle",
                "WAKO Thane is the local home of disciplined kickboxing - connecting athletes, coaches, academies, referees, and supporters through WAKO-aligned training, championships, and development pathways.",
            ),
            "contact_email": SiteSettings.get("contact_email", "info@wakothane.com"),
            "contact_phone": SiteSettings.get("contact_phone", "+91 00000 00000"),
            "contact_address": SiteSettings.get("contact_address", "Thane, Maharashtra, India"),
        },
        "current_year": timezone.now().year,
    }
