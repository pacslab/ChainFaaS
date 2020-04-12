from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from profiles.forms import UserForm, ChangeInfoForm
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from providers_app.views import initialize_rabbitmq_user
import fabric.views as fabric
from developers_app.models import Services
from django.contrib.auth.models import User


def index(request):
    """
    There is no page assigned to profiles index so we render the main index.html file.
    """
    return render(request, 'index.html')

@csrf_exempt
def register(request):
    """
    Registration page which shows a form for the user to complete
    """
    registered = False
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        if user_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            if user_form.cleaned_data['is_developer']:
                user.developer.active = True
                add_default_service(user.developer)
            if user_form.cleaned_data['is_provider']:
                user.provider.active = True
                # When a new provider is registered,
                # a new rabbitmq user should be added to the system
                initialize_rabbitmq_user(user)
                # TODO: create hyperledger fabric user
            r = fabric.invoke_new_monetary_account(user.username, '700')
            if 'jwt expired' in r.text or 'jwt malformed' in r.text or 'User was not found' in r.text:
                token = fabric.register_user()
                r = fabric.invoke_new_monetary_account(user.username, '700', token = token)
            user.save()
            registered = True
            if user_form.cleaned_data['is_provider']:
                return render(request, 'providers_app/index.html')
        else:
            print(user_form.errors)

    else:
        user_form = UserForm()
    return render(request, 'profiles/registration.html',
                           {'user_form': user_form,
                            'registered': registered})


def add_default_service(developer):
    default_service = Services.objects.create(developer=developer, provider=None, name="Test Function",
     docker_container="https://cloud.docker.com/u/ghaemisr/repository/docker/ghaemisr/node-info", active=True)
    default_service.save()

@login_required
def change_info(request):
    """
    If user is logged in, and they want to change their information, they will visit this page.
    """
    if request.method == 'POST':
        user_form = ChangeInfoForm(data=request.POST, instance=request.user)
        if user_form.is_valid():
            user = request.user
            if user_form.cleaned_data['is_developer']:
                user.developer.active = True
            else:
                user.developer.active = False
            if user_form.cleaned_data['is_provider']:
                user.provider.active = True
                initialize_rabbitmq_user(user)
            else:
                user.provider.active = False
            user.save()
        else:
            print(user_form.errors)

    else:
        user_form = ChangeInfoForm(initial={'username': request.user.username, 
                                            'email': request.user.email, 
                                            'is_developer': request.user.developer.active, 
                                            'is_provider': request.user.provider.active})

    return render(request, 'profiles/change_info.html',
                  {'user_form': user_form})


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('profiles:index'))


@csrf_exempt
def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                messages.success(request, "Successful Login")
                return HttpResponseRedirect(reverse('profiles:index'))
            else:
                # If account is not active:
                return HttpResponse("Your account is not active.")
        else:
            messages.error(request, "Invalid username or password")
            return render(request, 'profiles/login.html', {})

    else:
        # Nothing has been provided for username or password.
        return render(request, 'profiles/login.html', {})

def delete_test_users(request):
    test_users = User.objects.filter(username__startswith='test').delete()
    temp = len(User.objects.filter(username__startswith='test'))
    return HttpResponse(temp)