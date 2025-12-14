from django.urls import path
from . import views

app_name = 'auth_app'

urlpatterns = [
     path('profile/', views.profile, name='profile'),
     path('profile/edit/', views.edit_profile, name='edit_profile'),
     path('change-password/', views.change_password, name='change_password'),
     path('logout-confirm/', views.logout_confirm, name='logout_confirm'),
 ]
  
