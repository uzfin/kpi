from django.urls import path
from dashboard.views.main_views import DashboardView
from dashboard.views.kpi_views import (
    KPIView, KPIDetailView, KPICreateView, KPIDeleteView, KPIUpdateView,
)
# from dashboard.views.metric_views import (
#     MetricsView, MetricCreateView, MetricDetailView, 
#     MetricDeleteView, MetricUpdateView, MetricsAPIView,
# )
# from dashboard.views.submission_views import (
#     SubmissionsView, SubmissionCreateView, SubmissionDetailView,
#     SubmissionUpdateView, SubmissionDeleteView,
#     WorksView, WorkDetailView,
#     AssessmentView,
# )
# from dashboard.views.department_views import (
#     DepartmentView,
# )
# from dashboard.views.employee_views import (
#     EmployeeView,
# )
# from dashboard.views.notefication_views import (
#     SendNoteficationView, NoteficationView, SeeNoteficationView,
# )


app_name = "dashboard"

urlpatterns = [
    path("", DashboardView.as_view(), name="main"),

    path("kpis/", KPIView.as_view(), name="kpi"),
    path("kpis/<int:kpi_id>/", KPIDetailView.as_view(), name="kpi-detail"),
    path("kpis/create/", KPICreateView.as_view(), name="kpi-create"),
    path("kpis/delete/<int:kpi_id>/", KPIDeleteView.as_view(), name="kpi-delete"),
    path("kpis/update/<int:kpi_id>/", KPIUpdateView.as_view(), name="kpi-update"),

    # path("metrics/<int:kpi_id>/", MetricsView.as_view(), name="metrics"),
    # path("metrics/create/<int:kpi_id>/", MetricCreateView.as_view(), name="metric-create"),
    # path("metrics/<int:kpi_id>/<int:metric_id>/", MetricDetailView.as_view(), name="metric-detail"),
    # path("metrics/delete/<int:kpi_id>/<int:metric_id>/", MetricDeleteView.as_view(), name="metric-delete"),
    # path("metrics/update/<int:kpi_id>/<int:metric_id>/", MetricUpdateView.as_view(), name="metric-update"),

    # path("submissions/", SubmissionsView.as_view(), name="submissions"),
    # path("submissions/create/<int:kpi_id>/<int:metric_id>/", SubmissionCreateView.as_view(), name="submission-create"),
    # path("submissions/<int:submission_id>/", SubmissionDetailView.as_view(), name="submission-detail"),
    # path("submissions/update/<int:submission_id>/", SubmissionUpdateView.as_view(), name="submission-edit"),
    # path("submissions/delete/<int:submission_id>/", SubmissionDeleteView.as_view(), name="submission-delete"),

    # path("departments/", DepartmentView.as_view(), name="departments"),

    # path("employees/<int:department_id>/", EmployeeView.as_view(), name="employees"),

    # path("notefications/", NoteficationView.as_view(), name="get-notefications"),
    # path("notefications/<int:employee_id>/", SendNoteficationView.as_view(), name="notefications"),
    # path("notefications/see/<int:notefication_id>/", SeeNoteficationView.as_view(), name="see-notefication"),

    # path("works/", WorksView.as_view(), name="works"),
    # path("works/<int:work_id>/", WorkDetailView.as_view(), name="work-detail"),

    # path("assessment/<int:work_id>/", AssessmentView.as_view(), name="assessment"),

    # path("metrics/api/", MetricsAPIView.as_view(), name="metrics-api"),
]
