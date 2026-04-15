from django.shortcuts import render

# Create your views here.
def leave(request):
    """Render the leave page."""
    return render(request, 'leave/leave.html', { 'segment': 'Leave' })