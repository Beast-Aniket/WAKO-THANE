"""
Run this script once to create the admin superuser:
  .\\venv\\Scripts\\python.exe seed_admin.py
"""
import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'wako_thane.settings')
django.setup()

from users.models import User

if not User.objects.filter(username='admin').exists():
    u = User.objects.create_superuser(
        username='admin',
        email='admin@wakothane.com',
        password='admin@1234',
        role='ADMIN',
    )
    print(f"Superuser created: {u.username} / admin@1234")
else:
    print("Admin user already exists.")
