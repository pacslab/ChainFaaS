from django.shortcuts import render
from providers_app.views import add_task_to_queue
from profiles.models import Provider
from random import randint
import re
from datetime import datetime, timedelta
from providers_app.models import Job
from django.http import HttpResponse
import fabric.views as fabric
from pytz import timezone
from MSc_Research_Django.settings import TIME_ZONE


def request_handler(request, service, start_time):
    """
    Gets the request and the corresponding service and returns the response and the corresponding provider
    :param request:
    :param service:
    :return: If a provider exists, returns response, provider.
             If there is no appropriate provider, returns None, None.
    """
    provider = find_provider()
    if provider is None:
        return None, None, None, None

    job = Job.objects.create(provider=provider, service=service, start_time=start_time)
    # job.start_time = start_time
    job.save()
    task_link = service.docker_container
    task = re.search(r"/docker/(.*)$", task_link).group(1)
    task_developer = service.developer.id

    r = fabric.invoke_new_job(str(job.id), str(service.id), service.developer.user.username,
                                     provider.user.username, provider.fabric_org)
    if 'jwt expired' in r.text or 'jwt malformed' in r.text or 'User was not found' in r.text:
        token = fabric.register_user()
        r = fabric.invoke_new_job(str(job.id), str(service.id), service.developer.user.username,
                                     provider.user.username, provider.fabric_org)

    task_dict = {'task': task, 'task_developer':task_developer, 'job':job.id}
    response = add_task_to_queue(request, task_dict, provider.user.username)
    # total_time = response['pull_time'] + response['run_time']
    print("response from provider: ", response)
    job.refresh_from_db()
    job.pull_time = response['pull_time']
    job.run_time = response['run_time']
    job.total_time = response['total_time']
    job.cost = calculate_cost(response['total_time'])
    job.finished = True
    job.save()
    providing_time = int(((job.ack_time - job.start_time)/timedelta(microseconds=1))/1000) # Providing time in milliseconds
    r = fabric.invoke_received_result(str(job.id))
    if 'jwt expired' in r.text or 'jwt malformed' in r.text or 'User was not found' in r.text:
        token = fabric.register_user()
        r = fabric.invoke_received_result(str(job.id))
    return response, provider.user.username, providing_time, str(job.id)


def find_provider():
    """
    Finds an active provider who is ready to serve in the network. Returns an appropriate provider or None if it
    can't find any.
    :return: If a provider exists returns username.
             If there is no appropriate provider, returns None.
    """
    ready_providers = Provider.objects.filter(active=True, ready=True,
                                              last_ready_signal__gte=datetime.now(tz=timezone(TIME_ZONE)) - timedelta(minutes=1))
    if len(ready_providers) == 0:
        return
    random_index = randint(0, len(ready_providers) - 1)
    return ready_providers[random_index]

def calculate_cost(total_time):
    return total_time*0.01


def job_status(request):
    if request.method == 'GET':
        job_id = request.GET['Job'] 
        try:
            job = Job.objects.get(pk=job_id)
            return HttpResponse(str(job.finished))
        except:
            return HttpResponse('Job {} does not exist.'.format(job_id))
        

# def delete_all_jobs(request):
#     test_users = Job.objects.all()
#     temp = len(test_users)
#     test_users.delete()
#     return HttpResponse(temp)