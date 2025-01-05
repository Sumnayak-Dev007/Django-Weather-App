from django.contrib.auth import login,logout
from django.shortcuts import render,redirect
from .forms import UserForm
from django.contrib.auth.forms import AuthenticationForm
from Weatherapp.middlewares import auth,guest
# Create your views here.
@guest
def Register(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
              # Automatically log in the user after registration
            return redirect('login')
        else:
            print(form.errors)
    else:
        form = UserForm()
    context = {'form': form}
    return render(request, 'User/register.html', context)
   
@guest
def Login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request,data=request.POST)
        if form.is_valid():
            # Authenticate and log in the user
            user = form.get_user()
            login(request, user)
            return redirect('weather')  # Redirect to a success page
    else:
        form = AuthenticationForm()
    
    return render(request, 'User/login.html', {'form': form})

def Logout(request):
    logout(request)
    return redirect('login')