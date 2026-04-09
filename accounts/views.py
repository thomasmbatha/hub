# accounts/views.py

# ----------------------
# IMPORTS
# ----------------------
from django.shortcuts import render, redirect
from .models import OTP
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
from django.conf import settings
from twilio.rest import Client
from django.contrib.auth.views import (
    LoginView, PasswordResetView,
    PasswordResetConfirmView, PasswordChangeView
)
from .forms import (
    RegistrationForm,
    LoginForm,
    UserPasswordResetForm,
    UserSetPasswordForm,
    UserPasswordChangeForm
)

User = get_user_model()

# ----------------------
# FUNCTION-BASED VIEWS
# ----------------------

# ----- REGISTRATION -----
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.role = 'employee'  # Force role
            user.save()
            return redirect('login')
    else:
        form = RegistrationForm()
    return render(request, 'accounts/register.html', {'form': form})


# ----- LOGOUT -----
def logout_view(request):
    logout(request)
    return redirect('login')


# ----------------------
# CLASS-BASED VIEWS
# ----------------------

class UserLoginView(LoginView):
    template_name = 'accounts/login.html'
    form_class = LoginForm  # Use your custom form

    def form_valid(self, form):
        remember_me = self.request.POST.get('remember_me')
        response = super().form_valid(form)

        # If "remember me" is checked, save username in cookie
        if remember_me:
            response.set_cookie(
                'remembered_username', 
                form.cleaned_data.get('username'), 
                max_age=1209600  # 2 weeks
            )
        else:
            # Remove cookie if "remember me" is unchecked
            response.delete_cookie('remembered_username')

        # Set session expiry
        if remember_me:
            self.request.session.set_expiry(1209600)  # 2 weeks
        else:
            self.request.session.set_expiry(0)  # Session ends on browser close

        return response

    def get_success_url(self):
        next_url = self.request.GET.get('next')
        if next_url:
            return next_url

        user = self.request.user
        if hasattr(user, 'role'):
            if user.role == 'admin':
                return reverse_lazy('admin_dashboard')
            elif user.role == 'supervisor':
                return reverse_lazy('supervisor_dashboard')
        return reverse_lazy('index')

# ----- PASSWORD RESET REQUEST -----
class UserPasswordResetView(PasswordResetView):
    template_name = 'accounts/password_reset.html'          # your page
    form_class = UserPasswordResetForm
    email_template_name = 'accounts/password_reset_email.txt'   # plain fallback
    html_email_template_name = 'accounts/password_reset_email.html'  # HTML version
    subject_template_name = 'accounts/password_reset_subject.txt'
    success_url = reverse_lazy('password_reset_done')

# ----- PASSWORD RESET CONFIRM -----
class UserPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'accounts/password_reset_confirm.html'
    form_class = UserSetPasswordForm
    success_url = reverse_lazy('password_reset_complete')


# ----- PASSWORD CHANGE -----
class UserPasswordChangeView(PasswordChangeView):
    template_name = 'accounts/password_change.html'
    form_class = UserPasswordChangeForm
    success_url = reverse_lazy('index')

# ----------------------
# OTP VIEWS
# ----------------------

# ----- OTP request -----
def request_otp(request):
    if request.method == "POST":
        phone = request.POST.get("phone")
        phone = normalize_phone(request.POST.get("phone"))

        # Check recent OTP (1-minute cooldown)
        recent_otp = OTP.objects.filter(
            phone_number=phone,
            created_at__gte=timezone.now() - timedelta(minutes=1)
        ).exists()
        if recent_otp:
            return render(request, "accounts/request_otp.html", {"error": "Wait before requesting another OTP"})

        # Generate OTP
        code = OTP.generate_code()
        OTP.objects.create(phone_number=phone, code=code)

        # Send SMS
        client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
        client.messages.create(
            body=f"Your OTP is {code}",
            from_=settings.TWILIO_PHONE_NUMBER,
            to=phone
        )

        return redirect(f"/accounts/verify-otp/?phone={phone}")

    return render(request, "accounts/request_otp.html")

# ----- OTP verify -----
def verify_otp(request):
    if request.method == "POST":
        phone = normalize_phone(request.POST.get("phone"))
        code = request.POST.get("code")

        print("Normalized phone:", phone)
        print("Code entered:", code)
        print("OTP in DB:", list(OTP.objects.filter(phone_number=phone).values_list('code', flat=True)))

        otp = OTP.objects.filter(
            phone_number=phone,
            code=code,
            created_at__gte=timezone.now() - timedelta(minutes=5)
        ).order_by('-created_at').first()

        if otp:
            user, created = User.objects.get_or_create(username=phone)
            
            # IMPORTANT: set backend when manually logging in
            user.backend = 'django.contrib.auth.backends.ModelBackend'
            login(request, user)

            otp.delete()
            return redirect("index")

        return render(request, "accounts/verify_otp.html", {"error": "Invalid or expired OTP", "phone": phone})

    # GET request
    phone = normalize_phone(request.GET.get("phone", ""))
    return render(request, "accounts/verify_otp.html", {"phone": phone})

# OTP ----- Helper functions -----
def normalize_phone(phone):
    """
    Convert phone to proper E.164 format:
    '081 234 5678' -> '+27812345678'
    Removes spaces, dashes, parentheses.
    """
    if not phone:
        return ""
    # Remove all characters except digits
    digits = "".join(c for c in phone if c.isdigit())
    
    # Convert local numbers starting with 0 to +27
    if digits.startswith("0"):
        digits = "+27" + digits[1:]
    elif not digits.startswith("+"):
        digits = "+" + digits
    
    return digits