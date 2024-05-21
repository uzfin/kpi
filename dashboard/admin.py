from django.contrib import admin
from .models import (
    KPI,
    Criterion,
    Clause,
    Submission,
    Notefication,
    Mark,
    Result,
)


admin.site.register(
    (
        KPI,
        Criterion,
        Clause,
        Submission,
        Notefication,
        Mark,
        Result,
    )
)
