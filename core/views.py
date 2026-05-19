from django.contrib import messages
from django.shortcuts import redirect, render
from django.utils import timezone

from core.models import ContactMessage, SiteSettings
from events.models import Event
from gallery.models import GalleryItem
from members.models import Member
from users.models import User


DEFAULT_HERO_TITLE = "Train hard. Fight smart. Represent Thane."
DEFAULT_HERO_SUBTITLE = (
    "WAKO Thane is the local home of disciplined kickboxing - connecting athletes, coaches, "
    "academies, referees, and supporters through WAKO-aligned training, championships, and development pathways."
)


def home(request):
    upcoming_events = Event.objects.filter(date__gte=timezone.now()).order_by('date')[:3]
    featured_members = Member.objects.all()[:4]

    context = {
        'hero_title': SiteSettings.get('hero_title', DEFAULT_HERO_TITLE),
        'hero_subtitle': SiteSettings.get('hero_subtitle', DEFAULT_HERO_SUBTITLE),
        'latest_events': upcoming_events,
        'featured_members': featured_members,
        'gallery_preview': GalleryItem.objects.order_by('-uploaded_at')[:6],
        'player_count': User.objects.filter(role='PLAYER').count(),
        'academy_count': User.objects.filter(role='ACADEMY').count(),
        'member_count': Member.objects.count(),
        'event_count': Event.objects.count(),
    }
    return render(request, 'core/home.html', context)


def about(request):
    context = {
        'contact_email': SiteSettings.get('contact_email', 'info@wakothane.com'),
        'contact_phone': SiteSettings.get('contact_phone', '+91 00000 00000'),
        'contact_address': SiteSettings.get('contact_address', 'Thane, Maharashtra, India'),
        'member_count': Member.objects.count(),
        'event_count': Event.objects.count(),
        'gallery_count': GalleryItem.objects.count(),
    }
    return render(request, 'core/about.html', context)


def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        message = request.POST.get('message', '').strip()
        if name and email and message:
            ContactMessage.objects.create(name=name, email=email, message=message)
            messages.success(request, 'Your message has been sent! We will get back to you soon.')
            return redirect('contact')
        else:
            messages.error(request, 'Please fill in all fields.')
    context = {
        'contact_email': SiteSettings.get('contact_email', 'info@wakothane.com'),
        'contact_phone': SiteSettings.get('contact_phone', '+91 00000 00000'),
        'contact_address': SiteSettings.get('contact_address', 'Thane, Maharashtra, India'),
    }
    return render(request, 'core/contact.html', context)


def gallery_view(request):
    items = GalleryItem.objects.all().order_by('-uploaded_at')
    return render(request, 'core/gallery.html', {'items': items})


def events_view(request):
    now = timezone.now()
    upcoming = Event.objects.filter(date__gte=now).order_by('date')
    past = Event.objects.filter(date__lt=now).order_by('-date')
    return render(request, 'core/events.html', {'upcoming': upcoming, 'past': past})


def members_view(request):
    members_list = Member.objects.all()
    return render(request, 'core/members.html', {'members': members_list})
