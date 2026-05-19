"""
Run this script from the project root to create demo content:
  .\\venv\\Scripts\\python.exe seed_demo_content.py
"""

import os
from datetime import timedelta
from pathlib import Path

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "wako_thane.settings")
django.setup()

from django.core.files import File
from django.utils import timezone

from core.models import SiteSettings
from events.models import Event
from gallery.models import GalleryItem
from members.models import Member
from users.models import User


BASE_DIR = Path.cwd()
STATIC_DIR = BASE_DIR / "static"


def save_image(field_file, source_name, target_name):
    source_path = STATIC_DIR / source_name
    if not source_path.exists():
        return False

    current_name = Path(field_file.name).name if field_file and field_file.name else ""
    if current_name == target_name:
        return False

    with source_path.open("rb") as image_file:
        field_file.save(target_name, File(image_file), save=False)
    return True


def ensure_user(username, password, role, email, first_name, phone, is_superuser=False):
    user = User.objects.filter(username=username).first()
    created = False

    if not user:
        user = User(username=username)
        created = True

    user.email = email
    user.first_name = first_name
    user.role = role
    user.phone = phone
    user.is_staff = is_superuser
    user.is_superuser = is_superuser
    user.set_password(password)

    user.save()
    return user, created


SiteSettings.set("hero_title", "Train hard. Fight smart. Represent Thane.")
SiteSettings.set(
    "hero_subtitle",
    "WAKO Thane is the local home of disciplined kickboxing - connecting athletes, coaches, academies, referees, and supporters through WAKO-aligned training, championships, and development pathways.",
)
SiteSettings.set("contact_email", "info@wakothane.com")
SiteSettings.set("contact_phone", "+91 93210 44556")
SiteSettings.set("contact_address", "WAKO Thane Coordination Desk, Thane West, Maharashtra")

users = [
    {
        "username": "admin",
        "password": "admin@1234",
        "role": "ADMIN",
        "email": "admin@wakothane.com",
        "first_name": "Admin",
        "phone": "+91 93210 44556",
        "is_superuser": True,
    },
    {
        "username": "academy_demo",
        "password": "academy@1234",
        "role": "ACADEMY",
        "email": "academy@wakothane.com",
        "first_name": "Thane Fight Club",
        "phone": "+91 98198 22011",
        "is_superuser": False,
    },
    {
        "username": "player_demo",
        "password": "player@1234",
        "role": "PLAYER",
        "email": "player@wakothane.com",
        "first_name": "Aarav",
        "phone": "+91 98920 11045",
        "is_superuser": False,
    },
]

for user_data in users:
    user, created = ensure_user(**user_data)
    if created:
        print(f"Created user: {user.username}")
    else:
        print(f"Updated user profile: {user.username}")


member_data = [
    ("Rajesh Patil", "President", "1000453732.jpeg", "member-president.jpg"),
    ("Meera Naik", "General Secretary", "1000456564.jpeg", "member-secretary.jpg"),
    ("Imran Shaikh", "Technical Director", "1000452560.jpeg", "member-technical-director.jpg"),
    ("Priya More", "Athlete Development Coordinator", "1000451959.jpeg", "member-athlete-coordinator.jpg"),
]

for name, position, image_name, upload_name in member_data:
    member = Member.objects.filter(name=name, position=position).first()
    if not member:
        member = Member(name=name, position=position)
    if save_image(member.image, image_name, upload_name):
        print(f"Attached image for member: {name}")
    member.save()


gallery_data = [
    ("Ring action during a WAKO Thane bout", "1000452560.jpeg", "gallery-bout-action.jpg"),
    ("Championship medals ready for podium winners", "1000451959.jpeg", "gallery-medals.jpg"),
    ("Young athletes celebrating podium finishes", "1000453732.jpeg", "gallery-youth-podium.jpg"),
    ("Fight day focus before stepping onto the mat", "1000456564.jpeg", "gallery-fight-day-focus.jpg"),
]

for caption, image_name, upload_name in gallery_data:
    item = GalleryItem.objects.filter(caption=caption).first()
    if not item:
        item = GalleryItem(caption=caption)
    if save_image(item.image, image_name, upload_name):
        print(f"Attached gallery image: {caption}")
    item.caption = caption
    item.save()


now = timezone.now()
event_data = [
    {
        "title": "WAKO Thane District Selection Trials 2026",
        "date": now + timedelta(days=10, hours=9),
        "description": "Official district selection trials for point fighting, kick light, and low kick divisions. Athlete reporting, document checks, and weigh-ins begin in the morning.",
        "image_name": "1000452560.jpeg",
        "upload_name": "event-district-selection-trials.jpg",
    },
    {
        "title": "Youth Kickboxing Coaching Camp",
        "date": now + timedelta(days=18, hours=7),
        "description": "A focused development camp for youth athletes covering ring discipline, footwork, defensive basics, and competition etiquette under WAKO-style guidance.",
        "image_name": "1000456564.jpeg",
        "upload_name": "event-youth-coaching-camp.jpg",
    },
    {
        "title": "Officials and Referee Development Clinic",
        "date": now + timedelta(days=25, hours=6),
        "description": "Technical clinic for referees, judges, and event volunteers with rule refreshers, bout control standards, and scoring practice for tatami and ring sport.",
        "image_name": "1000453732.jpeg",
        "upload_name": "event-officials-clinic.jpg",
    },
    {
        "title": "Inter-Academy Ring and Tatami League",
        "date": now + timedelta(days=33, hours=8),
        "description": "Friendly inter-academy competition day designed to build ring confidence, mat discipline, and visibility for participating clubs and athletes across Thane.",
        "image_name": "1000451959.jpeg",
        "upload_name": "event-inter-academy-league.jpg",
    },
    {
        "title": "Thane Open Kickboxing Championship 2026",
        "date": now - timedelta(days=21),
        "description": "A completed championship showcase featuring youth and senior divisions, podium moments, and strong participation from local academies and independent athletes.",
        "image_name": "1000451959.jpeg",
        "upload_name": "event-thane-open-championship.jpg",
    },
]

for event_info in event_data:
    event = Event.objects.filter(title=event_info["title"]).first()
    if not event:
        event = Event(title=event_info["title"])
    event.date = event_info["date"]
    event.description = event_info["description"]
    if save_image(event.poster_image, event_info["image_name"], event_info["upload_name"]):
        print(f"Attached poster for event: {event.title}")
    event.save()


print("")
print("Demo content ready.")
print("Test logins:")
print("  Admin   : admin / admin@1234")
print("  Academy : academy_demo / academy@1234")
print("  Player  : player_demo / player@1234")
print(f"Events  : {Event.objects.count()}")
print(f"Gallery : {GalleryItem.objects.count()}")
print(f"Members : {Member.objects.count()}")
