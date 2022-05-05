from django.shortcuts import render, redirect
from static.python.CustomUserCreationForm import RegisterForm
from static.python.UserForms import RegisterForm, UserLogin


def register(request):
    if request.method == 'POST':
        form = RegisterForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = RegisterForm()

    return render(request, 'user/register.html', {
        'form': form
    })


def login(request):
    form = UserLogin()
    if form.is_valid():
        form.save()
        return redirect('login')

    return render(request, 'user/login.html', {
        'form': form
    })
