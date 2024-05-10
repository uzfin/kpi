from django.shortcuts import render
from users.models import User
from dashboard.models import Submission, Department, Metric


def landing_page(request):

    ctx = {
        'users': User.objects.all(),
        'submissions': Submission.objects.all(),
        'departments': Department.objects.all(),
        'metrics': Metric.objects.all(),
    }
    return render(request, 'landing.html', ctx)
