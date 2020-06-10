from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from developers_app.forms import ServiceForm
from django.contrib import messages
from django.db import IntegrityError
from developers_app.models import Services
from providers_app.models import Job
from django.core.exceptions import ObjectDoesNotExist
from controller_app.views import request_handler
from datetime import datetime
from pytz import timezone
from MSc_Research_Django.settings import TIME_ZONE


def index(request):
    return render(request, 'developers_app/index.html')


@login_required()
def new_service(request):
    """
    Creates a new service in the network.
    """
    if request.method == 'POST':
        service_form = ServiceForm(data=request.POST)
        if service_form.is_valid():
            service = service_form.save(commit=False)
            service.developer = request.user.developer
            service.provider = None
            service.active = True
            try:
                service.save()
                messages.success(request, "New service created")
                service_form = ServiceForm()
            except IntegrityError:
                messages.error(request, "You already have a service with this name")
        else:
            print(service_form.errors)
    else:
        service_form = ServiceForm()

    return render(request, 'developers_app/new_service.html',
                  {'service_form': service_form})


@login_required()
def user_services(request):
    """
    Shows all services owned by a user.
    """
    all_services = Services.objects.filter(developer=request.user.developer)

    return render(request, 'developers_app/user_services.html',
                  {'all_services': all_services,
                   'developer_id': request.user.developer.id})

@login_required()
def stop_service(request, service_id):
    all_services = Services.objects.filter(developer=request.user.developer)
    service = Services.objects.get(id=service_id)
    service.active = False
    service.save()
    return render(request, 'developers_app/services_table.html',
                  {'all_services': all_services,
                   'developer_id': request.user.developer.id})


@login_required()
def start_service(request, service_id):
    service = Services.objects.get(id=service_id)
    all_services = Services.objects.filter(developer=request.user.developer)
    service.active = True
    service.save()
    return render(request, 'developers_app/services_table.html',
                  {'all_services': all_services,
                   'developer_id': request.user.developer.id})


@login_required()
def delete_service(request, service_id):
    all_services = Services.objects.filter(developer=request.user.developer)
    service = Services.objects.get(id=service_id)
    service.delete()
    return render(request, 'developers_app/services_table.html',
                  {'all_services': all_services,
                   'developer_id': request.user.developer.id})


def run_service(request, service_id):
    response = ''
    try:
        service = Services.objects.get(id=service_id)
        if service.active:
            temp_time = datetime.now(tz=timezone(TIME_ZONE))
            response, provider, providing_time, job_id = request_handler(request, service, temp_time)
            if response is None:
                messages.error(request, "There are no available providers in the network")
                return redirect('index')
            else:
                messages.success(request, "Successfully sent a request to '{}' service of '{}'".format(service.name,
                                                                                                   service.developer))
        else:
            messages.error(request, "This service is disabled")

    except ObjectDoesNotExist:
        messages.error(request, "Incorrect service id")

    return render(request, 'final_response.html',
                  {'result': response['Result'],
                   'providing_time': providing_time,
                   'pull_time': response['pull_time'],
                   'run_time': response['run_time'],
                   'total_time': response['total_time'],
                   'provider': provider, 
                   'job_id': job_id})

@login_required()
def user_jobs(request):
    """
    Shows all jobs that belong to a user.
    """
    services = Services.objects.filter(developer=request.user.developer)
    all_jobs = Job.objects.filter(service__in=services).order_by('pk').reverse()
    return render(request, 'developers_app/user_jobs.html',
                  {'all_jobs': all_jobs,
                   'developer_id': request.user.developer.id})
