from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views import View

# Create your views here.
from django.views.generic import FormView
from .forms import UserRegistrationForm, UserUpdateForm
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, LogoutView
# Create your views here.

class UserRegistrationView(FormView):
    template_name = 'accounts/register.html'
    form_class = UserRegistrationForm
    success_url = reverse_lazy('update_profile')
    
    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return super().form_valid(form)  # if all is okay than form_valid function is called
    
    
    
    
class UserLoginView(LoginView):
    template_name = 'accounts/signin.html'
    
    def get_success_url(self):
        return reverse_lazy('home')
    

class UserLogoutView(LogoutView):
    def get_success_url(self):
        if self.request.user.is_authenticated:
            logout(self.request)
        return reverse_lazy('home')
    
    
class UserAccountUpdateView(View):
    template_name = 'accounts/update_profile.html'
    
    def get(self, request):
        form = UserUpdateForm(instance = request.user)
        return render(request, self.template_name, {'form': form})
    
    def post(self, request):
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('update_profile')
        return render(request, self.template_name, {'form': form})
    
        

def get_create_session(request):
    if not request.session.session_key:
        request.session.create()
    return request.session.session_key
