# accounts/views.py

from django.shortcuts import render, redirect
from django.utils import timezone
from datetime import timedelta
from django.conf import settings

from django.contrib.auth import login, logout, get_user_model
from django.contrib.auth.views import (
    LoginView, PasswordResetView,
    PasswordResetConfirmView, PasswordChangeView
)

from twilio.rest import Client

from .models import OTP
from .forms import (
    RegistrationForm,
    LoginForm,
    UserPasswordResetForm,
    UserSetPasswordForm,
    UserPasswordChangeForm
)

User = get_user_model()

# ======================================================
# AUTH VIEWS
# ======================================================

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.role = 'employee'
            user.save()
            return redirect('login')
    else:
        form = RegistrationForm()

    return render(request, 'accounts/register.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('login')


class UserLoginView(LoginView):
    template_name = 'accounts/login.html'
    form_class = LoginForm

    def form_valid(self, form):
        remember_me = self.request.POST.get('remember_me')
        response = super().form_valid(form)

        if remember_me:
            response.set_cookie(
                'remembered_username',
                form.cleaned_data.get('username'),
                max_age=1209600
            )
            self.request.session.set_expiry(1209600)
        else:
            response.delete_cookie('remembered_username')
            self.request.session.set_expiry(0)

        return response

    def get_success_url(self):
        user = self.request.user

        if hasattr(user, 'role'):
            if user.role == 'admin':
                return '/admin-dashboard/'
            elif user.role == 'supervisor':
                return '/supervisor-dashboard/'

        return '/'


class UserPasswordResetView(PasswordResetView):
    template_name = 'accounts/password_reset.html'
    form_class = UserPasswordResetForm
    success_url = '/accounts/password-reset/done/'


class UserPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'accounts/password_reset_confirm.html'
    form_class = UserSetPasswordForm
    success_url = '/accounts/password-reset/complete/'


class UserPasswordChangeView(PasswordChangeView):
    template_name = 'accounts/password_change.html'
    form_class = UserPasswordChangeForm
    success_url = '/'


# ======================================================
# OTP SETTINGS
# ======================================================

COOLDOWN_SECONDS = 60


# ======================================================
# HELPERS
# ======================================================

def normalize_phone(phone):
    if not phone:
        return ""

    digits = "".join(c for c in phone if c.isdigit())

    if digits.startswith("0"):
        digits = "+27" + digits[1:]
    elif not digits.startswith("+"):
        digits = "+" + digits

    return digits


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        return x_forwarded_for.split(',')[0]
    return request.META.get('REMOTE_ADDR')


# ======================================================
# OTP REQUEST
# ======================================================

def request_otp(request):
    if request.method == "POST":
        phone = normalize_phone(request.POST.get("phone"))

        # -------------------------------
        # RATE LIMIT (IP BASED)
        # -------------------------------
        ip = get_client_ip(request)

        recent_requests = OTP.objects.filter(
            created_at__gte=timezone.now() - timedelta(minutes=10)
        ).count()

        if recent_requests > 20:
            return render(request, "accounts/request_otp.html", {
                "error": "Too many requests. Try again later."
            })

        # -------------------------------
        # COOLDOWN PER PHONE
        # -------------------------------
        latest_otp = OTP.objects.filter(
            phone_number=phone
        ).order_by('-created_at').first()

        if latest_otp:
            time_passed = (timezone.now() - latest_otp.created_at).total_seconds()

            if time_passed < COOLDOWN_SECONDS:
                remaining = int(COOLDOWN_SECONDS - time_passed)
                return render(request, "accounts/request_otp.html", {
                    "error": f"Wait {remaining}s before requesting another OTP",
                    "cooldown": remaining
                })

        # -------------------------------
        # CREATE OTP
        # -------------------------------
        code = OTP.generate_code()
        OTP.objects.create(phone_number=phone, code=code)

        # -------------------------------
        # SEND SMS (TWILIO)
        # -------------------------------
        client = Client(
            settings.TWILIO_ACCOUNT_SID,
            settings.TWILIO_AUTH_TOKEN
        )

        client.messages.create(
            body=f"Your OTP is {code}",
            from_=settings.TWILIO_PHONE_NUMBER,
            to=phone
        )

        return redirect(f"/accounts/verify-otp/?phone={phone}")

    return render(request, "accounts/request_otp.html")


# ======================================================
# OTP VERIFY
# ======================================================

def verify_otp(request):
    if request.method == "POST":
        phone = normalize_phone(request.POST.get("phone"))
        code = request.POST.get("code")

        otp = OTP.objects.filter(
            phone_number=phone,
            code=code,
            created_at__gte=timezone.now() - timedelta(minutes=5)
        ).order_by('-created_at').first()

        if otp:
            user, created = User.objects.get_or_create(username=phone)
            user.backend = 'django.contrib.auth.backends.ModelBackend'
            login(request, user)

            otp.delete()
            return redirect("index")

        return render(request, "accounts/verify_otp.html", {
            "error": "Invalid or expired OTP",
            "phone": phone
        })

    phone = normalize_phone(request.GET.get("phone", ""))
    return render(request, "accounts/verify_otp.html", {
        "phone": phone
    })