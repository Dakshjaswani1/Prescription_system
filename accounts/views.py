from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from .forms import CustomUserCreationForm

@login_required
def dashboard(request):
    user = request.user
    context = {}
    
    if user.role == 'Doctor':
        # Context for doctor dashboard
        # e.g., recent prescriptions
        pass
    elif user.role == 'Receptionist':
        # Context for receptionist
        # e.g., recent patients, pending prescriptions
        pass
    elif user.role == 'Admin':
        # Context for admin
        # e.g., low stock alerts
        pass
        
    return render(request, 'dashboard.html', context)

def signup(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
        
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = CustomUserCreationForm()
        
    return render(request, 'registration/signup.html', {'form': form})

