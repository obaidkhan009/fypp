from django.urls import path
from . import views
from .views import modelview
from django.contrib.auth import views as auth_views
from .views import payment_view


urlpatterns = [
    path('', views.index, name='index'),
    path('modelview', views.modelview, name='modelview'),
    path('login_view', views.login_view, name='login_view'),  # Keep this
    
    path('generate_images', views.generate_images, name='generate_images'),
    path('login_user', views.login_user, name='login_user'),
    path('logout', views.logout_user, name='logout'),
    path('signup', views.signup_view, name='signup'),
    path('feed', views.index, name='feed'),
    path('payment', views.payment_view, name='payment_view'),  # Ensure payment_view is in views.py
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]
