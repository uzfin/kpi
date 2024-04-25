from django.urls import path
from .views import (
    DashboardView, KPIView, KPICreateView, KPIDetailView, KPIDeleteView, KPIUpdateView, 
    MetricsView, MetricCreateView, MetricDetailView, MetricDeleteView, MetricUpdateView,
    SubmissionsView, #SubmissionCreateView
)


app_name = "dashboard"

urlpatterns = [
    path("", DashboardView.as_view(), name="main"),
    path("kpis/", KPIView.as_view(), name="kpi"),
    path("kpis/create/", KPICreateView.as_view(), name="kpi-create"),
    path("kpis/<int:kpi_id>/", KPIDetailView.as_view(), name="kpi-detail"),
    path("kpis/delete/<int:kpi_id>/", KPIDeleteView.as_view(), name="kpi-delete"),
    path("kpis/update/<int:kpi_id>/", KPIUpdateView.as_view(), name="kpi-update"),

    path("metrics/<int:kpi_id>/", MetricsView.as_view(), name="metrics"),
    path("metrics/create/<int:kpi_id>/", MetricCreateView.as_view(), name="metric-create"),
    path("metrics/<int:kpi_id>/<int:metric_id>/", MetricDetailView.as_view(), name="metric-detail"),
    path("metrics/delete/<int:kpi_id>/<int:metric_id>/", MetricDeleteView.as_view(), name="metric-delete"),
    path("metrics/update/<int:kpi_id>/<int:metric_id>/", MetricUpdateView.as_view(), name="metric-update"),

    path("submissions/", SubmissionsView.as_view(), name="submissions"),
    # path("submissions/create/", SubmissionCreateView.as_view(), name="submissino-create"),
]
