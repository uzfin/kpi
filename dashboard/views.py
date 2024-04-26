from datetime import date

from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from users.permissions import IsCEO, IsManager, IsEmployee
from django.views import View
from django.http import HttpRequest, HttpResponse, JsonResponse
from .forms import KPICreationForm, MetricCreationForm, SubmissionCreationForm

from .models import KPI, Notefication, Department, Metric
from users.models import User



