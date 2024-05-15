from django.contrib import admin
from .models import (
    KPI,
    Criterion,
    Clause,
    Submission,
    Notefication,
)


admin.site.register(
    (
        KPI,
        Criterion,
        Clause,
        Submission,
        Notefication,
    )
)
