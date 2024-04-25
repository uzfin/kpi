from django.urls import path
from .views import DashboardView, KPIView, KPICreateView, KPIDetailView, KPIDeleteView, KPIUpdateView


app_name = "dashboard"

urlpatterns = [
    path("", DashboardView.as_view(), name="main"),
    path("kpis/", KPIView.as_view(), name="kpi"),
    path("kpis/create/", KPICreateView.as_view(), name="kpi-create"),
    path("kpis/<int:kpi_id>/", KPIDetailView.as_view(), name="kpi-detail"),
    path("kpis/delete/<int:kpi_id>/", KPIDeleteView.as_view(), name="kpi-delete"),
    path("kpis/update/<int:kpi_id>/", KPIUpdateView.as_view(), name="kpi-update"),
]
