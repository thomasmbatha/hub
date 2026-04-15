# hub/home/views.py

# ----------------------
# IMPORTS
# ----------------------
from django.shortcuts import render

# ----------------------
# PAGE VIEWS (Function-Based)
# ----------------------
def index(request):
    """Render the dashboard/homepage."""
    return render(request, 'pages/index.html', { 'segment': 'home' })


def tables(request):
    """Render the tables page."""
    return render(request, 'pages/tables.html', { 'segment': 'tables' })

def vr(request):
    """Render the virtual reality demo page."""
    return render(request, 'pages/virtual-reality.html', { 'segment': 'virtual_reality' })

def rtl(request):
    """Render the right-to-left layout page."""
    return render(request, 'pages/rtl.html', { 'segment': 'rtl' })


