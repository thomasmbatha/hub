from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [

    # 🔐 Authentication
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register, name='register'),

    # 🔑 Password Change
    path('password-change/', views.UserPasswordChangeView.as_view(), name='password_change'),
    path('password-change-done/', auth_views.PasswordChangeDoneView.as_view(
        template_name='accounts/password_change_done.html'
    ), name="password_change_done"),

    # 🔄 Password Reset
    path('password-reset/', views.UserPasswordResetView.as_view(), name='password_reset'),

    path('password-reset-done/', auth_views.PasswordResetDoneView.as_view(
        template_name='accounts/password_reset_done.html'
    ), name='password_reset_done'),

    path('password-reset-confirm/<uidb64>/<token>/',
        views.UserPasswordResetConfirmView.as_view(),
        name='password_reset_confirm'),

    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(
        template_name='accounts/password_reset_complete.html'
    ), name='password_reset_complete'),

    # 🔄 Password Reset
    path("phone-login/", views.request_otp, name="phone_login"),
    path("verify-otp/", views.verify_otp, name="verify_otp"),

]