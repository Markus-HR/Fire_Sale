from django.shortcuts import render, redirect
from static.python.CustomUserForms import RegisterForm, LoginForm
# from static.python.UserForms import UserLogin
from django.contrib.auth.views import LoginView


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


class CustomLoginView(LoginView):
    form_class = LoginForm
