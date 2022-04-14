from django.contrib.auth import logout, authenticate, login
from django.http import HttpResponse
from django.shortcuts import render, redirect

from exchangeapp.models import Portfolio
from .forms import LoginForm, CustomUserCreationForm, ValueForm
from exchangeapp import views as vgames
# Create your views here.
from .models import CustomUser


def logout_view(request):
    logout(request)
    return redirect(vgames.main_page)


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(email=cd['email'], password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect(vgames.main_page)
                else:
                    return HttpResponse('Пользователь заблокирован')
            else:
                return HttpResponse('Данные введены неверно. Проверьте логин или пароль')
    else:
        form = LoginForm()
    return render(request, 'users/login.html', {'form': form})


def register(request):
    if request.method == 'POST':
        user_form = CustomUserCreationForm(request.POST)
        if user_form.is_valid():
            #создание нового пользователя
            new_user = user_form.save(commit=False)
            #Сохранение пароля
            new_user.set_password(user_form.cleaned_data['password1'])
            # Сохранение нового пользователя
            new_user.save()
            return render(request, 'users/register_done.html', {'new_user': new_user})
    else:
        user_form = CustomUserCreationForm()
    return render(request, 'users/1index.html', {'user_form': user_form})


def money(request, pk):
    user = CustomUser.objects.get(pk=pk)
    if request.method == 'GET':
        form = ValueForm()
        context = {'user': user, 'form':form}
        return render(request, 'users/money.html', context)
    elif request.method == 'POST':
        user_pk = CustomUser.objects.get(pk=pk)
        money_value = float(request.POST['value'])
        user_pk.money = float(user_pk.money) + money_value
        user_pk.save()
        context = {'value':money_value,'user': user_pk}
        return render(request,'users/money_success.html',context)


def portfolio_page(request):
    portfolio = Portfolio.objects.filter(user=request.user)
    context = {'portfolio_list': portfolio}
    return render(request, 'users/portfolio.html', context)






