from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('gallery/', views.gallery_view, name='gallery'),
    path('events/', views.events_view, name='events'),
    path('members/', views.members_view, name='members'),
]
