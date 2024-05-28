from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

def login_signup_view(request):
    if request.method == 'POST':
        if 'login' in request.POST:
            login_form = AuthenticationForm(request, data=request.POST)
            signup_form = UserCreationForm()
            if login_form.is_valid():
                username = login_form.cleaned_data.get('username')
                password = login_form.cleaned_data.get('password')
                user = authenticate(username=username, password=password)
                if user is not None:
                    login(request, user)
                    return redirect(f'/{user.username}/')
        elif 'signup' in request.POST:
            signup_form = UserCreationForm(request.POST)
            login_form = AuthenticationForm()
            if signup_form.is_valid():
                signup_form.save()
                username = signup_form.cleaned_data.get('username')
                password = signup_form.cleaned_data.get('password1')
                user = authenticate(username=username, password=password)
                login(request, user)
                return redirect(f'/{user.username}/')
    else:
        login_form = AuthenticationForm()
        signup_form = UserCreationForm()

    return render(request, 'accounts/login_signup.html', {'login_form': login_form, 'signup_form': signup_form})