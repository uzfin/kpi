from django.contrib import admin
from .models import (
    Department,
    KPI,
    Metric,
    Submission,
    Notefication,
    Result,
)


admin.site.register((
    Department,
    KPI,
    Metric,
    Submission,
    Notefication,
    Result,
))
