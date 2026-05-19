from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('dashboard/gallery/', views.dashboard_gallery, name='dashboard_gallery'),
    path('dashboard/events/', views.dashboard_events, name='dashboard_events'),
    path('dashboard/members/', views.dashboard_members, name='dashboard_members'),
    path('dashboard/academy/', views.dashboard_academy, name='dashboard_academy'),
    path('dashboard/player/', views.dashboard_player, name='dashboard_player'),
]
