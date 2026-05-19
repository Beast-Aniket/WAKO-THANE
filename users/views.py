from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.utils import timezone

from events.models import Event
from .models import User


def login_view(request):
    if request.user.is_authenticated:
        return redirect_by_role(request.user)

    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back, {user.first_name or user.username}!')
            return redirect_by_role(user)
        else:
            messages.error(request, 'Invalid username or password. Please try again.')

    return render(request, 'users/login.html')


def register_view(request):
    if request.user.is_authenticated:
        return redirect_by_role(request.user)

    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')
        confirm_password = request.POST.get('confirm_password', '')
        role = request.POST.get('role', 'PLAYER')
        first_name = request.POST.get('first_name', '').strip()
        phone = request.POST.get('phone', '').strip()

        # Validation
        if password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'users/register.html', {'form_data': request.POST})

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already taken. Please choose another.')
            return render(request, 'users/register.html', {'form_data': request.POST})

        if User.objects.filter(email=email).exists():
            messages.error(request, 'An account with this email already exists.')
            return render(request, 'users/register.html', {'form_data': request.POST})

        if len(password) < 6:
            messages.error(request, 'Password must be at least 6 characters long.')
            return render(request, 'users/register.html', {'form_data': request.POST})

        # Create user
        user = User.objects.create(
            username=username,
            email=email,
            first_name=first_name,
            password=make_password(password),
            role=role,
            phone=phone,
        )
        login(request, user)
        messages.success(request, f'Account created successfully! Welcome to WAKO THANE, {user.first_name or user.username}.')
        return redirect_by_role(user)

    return render(request, 'users/register.html')


def logout_view(request):
    if request.method == 'POST':
        logout(request)
        messages.info(request, 'You have been logged out.')
    return redirect('home')


def redirect_by_role(user):
    if user.role == 'ADMIN' or user.is_superuser:
        return redirect('dashboard')
    elif user.role == 'ACADEMY':
        return redirect('dashboard_academy')
    else:
        return redirect('dashboard_player')


# ─── Dashboard Views ───────────────────────────────────────────────────────────

def admin_required(view_func):
    """Decorator: redirect non-admins away from admin views."""
    from functools import wraps
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        if not (request.user.role == 'ADMIN' or request.user.is_superuser):
            messages.error(request, 'You do not have permission to access the admin dashboard.')
            return redirect('home')
        return view_func(request, *args, **kwargs)
    return wrapper


def role_required(*allowed_roles):
    """Decorator: redirect authenticated users away from dashboards outside their role."""
    def decorator(view_func):
        from functools import wraps

        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect('login')
            if request.user.role not in allowed_roles and not request.user.is_superuser:
                messages.error(request, 'Please use the dashboard assigned to your role.')
                return redirect_by_role(request.user)
            return view_func(request, *args, **kwargs)

        return wrapper

    return decorator


@admin_required
def dashboard_view(request):
    from events.models import Event
    from gallery.models import GalleryItem
    from members.models import Member
    from core.models import SiteSettings, ContactMessage

    if request.method == 'POST':
        hero_title = request.POST.get('hero_title', '')
        hero_subtitle = request.POST.get('hero_subtitle', '')
        contact_email = request.POST.get('contact_email', '')
        contact_phone = request.POST.get('contact_phone', '')
        contact_address = request.POST.get('contact_address', '')
        SiteSettings.set('hero_title', hero_title)
        SiteSettings.set('hero_subtitle', hero_subtitle)
        SiteSettings.set('contact_email', contact_email)
        SiteSettings.set('contact_phone', contact_phone)
        SiteSettings.set('contact_address', contact_address)
        messages.success(request, 'Home page settings updated successfully.')

    context = {
        'total_events': Event.objects.count(),
        'total_gallery': GalleryItem.objects.count(),
        'total_members': Member.objects.count(),
        'total_users': User.objects.count(),
        'unread_messages': ContactMessage.objects.filter(is_read=False).count(),
        'hero_title': SiteSettings.get('hero_title', 'Train hard. Fight smart. Represent Thane.'),
        'hero_subtitle': SiteSettings.get('hero_subtitle', 'WAKO Thane connects athletes, coaches, academies, referees, and supporters through recognised kickboxing pathways and event activity.'),
        'contact_email': SiteSettings.get('contact_email', 'info@wakothane.com'),
        'contact_phone': SiteSettings.get('contact_phone', '+91 93210 44556'),
        'contact_address': SiteSettings.get('contact_address', 'WAKO Thane Coordination Desk, Thane West, Maharashtra'),
    }
    return render(request, 'dashboard/admin_home.html', context)


@admin_required
def dashboard_gallery(request):
    from gallery.models import GalleryItem
    import os

    if request.method == 'POST':
        action = request.POST.get('action', 'add')
        if action == 'delete':
            item_id = request.POST.get('item_id')
            try:
                item = GalleryItem.objects.get(id=item_id)
                if item.image and os.path.isfile(item.image.path):
                    os.remove(item.image.path)
                item.delete()
                messages.success(request, 'Gallery image deleted.')
            except GalleryItem.DoesNotExist:
                messages.error(request, 'Image not found.')
        else:
            image = request.FILES.get('image')
            caption = request.POST.get('caption', '')
            if image:
                GalleryItem.objects.create(image=image, caption=caption)
                messages.success(request, 'Image added to gallery.')
            else:
                messages.error(request, 'Please select an image to upload.')

    items = GalleryItem.objects.all().order_by('-uploaded_at')
    return render(request, 'dashboard/admin_gallery.html', {'items': items})


@admin_required
def dashboard_events(request):
    from events.models import Event
    import os

    if request.method == 'POST':
        action = request.POST.get('action', 'add')
        if action == 'delete':
            event_id = request.POST.get('event_id')
            try:
                event = Event.objects.get(id=event_id)
                if event.poster_image and os.path.isfile(event.poster_image.path):
                    os.remove(event.poster_image.path)
                event.delete()
                messages.success(request, 'Event deleted successfully.')
            except Event.DoesNotExist:
                messages.error(request, 'Event not found.')
        else:
            title = request.POST.get('title', '').strip()
            date = request.POST.get('date', '')
            description = request.POST.get('description', '').strip()
            poster = request.FILES.get('poster_image')
            if title and date and description:
                Event.objects.create(
                    title=title,
                    date=date,
                    description=description,
                    poster_image=poster,
                )
                messages.success(request, f'Event "{title}" created successfully.')
            else:
                messages.error(request, 'Please fill in all required fields.')

    events = Event.objects.all().order_by('date')
    return render(request, 'dashboard/admin_events.html', {'events': events})


@admin_required
def dashboard_members(request):
    from members.models import Member
    import os

    if request.method == 'POST':
        action = request.POST.get('action', 'add')
        if action == 'delete':
            member_id = request.POST.get('member_id')
            try:
                member = Member.objects.get(id=member_id)
                if member.image and os.path.isfile(member.image.path):
                    os.remove(member.image.path)
                member.delete()
                messages.success(request, 'Member removed.')
            except Member.DoesNotExist:
                messages.error(request, 'Member not found.')
        else:
            name = request.POST.get('name', '').strip()
            position = request.POST.get('position', '').strip()
            image = request.FILES.get('image')
            if name and position:
                Member.objects.create(name=name, position=position, image=image)
                messages.success(request, f'Member "{name}" added.')
            else:
                messages.error(request, 'Name and position are required.')

    members_list = Member.objects.all()
    return render(request, 'dashboard/admin_members.html', {'members': members_list})


@role_required('ACADEMY')
def dashboard_academy(request):
    upcoming_events = Event.objects.filter(date__gte=timezone.now()).order_by('date')[:3]
    context = {
        'upcoming_events': upcoming_events,
    }
    return render(request, 'dashboard/academy_home.html', context)


@role_required('PLAYER')
def dashboard_player(request):
    upcoming_events = Event.objects.filter(date__gte=timezone.now()).order_by('date')[:3]
    context = {
        'upcoming_events': upcoming_events,
    }
    return render(request, 'dashboard/player_home.html', context)
