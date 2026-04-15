from django.shortcuts import render

def uniform(request):
    """Render the uniform page."""
    return render(request, 'uniform/uniform.html', { 'segment': 'Uniform Store' })