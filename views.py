from django.http import HttpResponse
from django.shortcuts import render
from .models import Todo
from .scheduling import *

tasks = []

# Create your views here.
def home(request):
    if request.method == 'POST':
        task=request.POST.get('task')
        task_input = Todo(task=task)
        # test script
        task = parse_task(str(task_input))
        tasks.append(task)
        accums, log = scheduled_calendars(tasks)
        render_log2(log, "monday")
        # new.save()
    return render(request,"index.html")

def individual_post(request):
    return HttpResponse(str(request))