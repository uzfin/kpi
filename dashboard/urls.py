from django.urls import path
from dashboard.views.main_views import DashboardView
from dashboard.views.kpi_views import (
    KPIView, KPIDetailView, KPICreateView, KPIDeleteView, KPIUpdateView,
)
from dashboard.views.criterion_views import (
    CriterionsView, CriterionsCreateView, CriterionDetailView, 
    CriterionDeleteView, CriterionUpdateView,
)
from dashboard.views.clause_views import (
    ClauseDetailView, ClauseCreateView, ClauseInternalCreateView,
    ClauseDeleteView, ClauseUpdateView,
)
from dashboard.views.submission_views import (
    SubmissionsView, SubmissionCreateView, SubmissionDetailView,
    SubmissionUpdateView, SubmissionDeleteView,
)
from dashboard.views.work_views import (
    WorksView, WorkDetailView,
    AssessmentView,
)
from dashboard.views.notefication_views import (
    SendNoteficationView, NoteficationView, SeeNoteficationView,
)
from dashboard.views.department_views import (
    DepartmentView, DepartmentCreateView,
    DepartmentDetailView, DepartmentDeleteView,
    DepartmentUpdateView,
)
from dashboard.views.employee_views import (
    EmployeeView,
)


app_name = "dashboard"

urlpatterns = [
    path("", DashboardView.as_view(), name="main"),

    path("kpis/", KPIView.as_view(), name="kpi"),
    path("kpis/<int:kpi_id>/", KPIDetailView.as_view(), name="kpi-detail"),
    path("kpis/create/", KPICreateView.as_view(), name="kpi-create"),
    path("kpis/delete/<int:kpi_id>/", KPIDeleteView.as_view(), name="kpi-delete"),
    path("kpis/update/<int:kpi_id>/", KPIUpdateView.as_view(), name="kpi-update"),

    path("criterions/<int:kpi_id>/", CriterionsView.as_view(), name="criterions"),
    path("criterions/create/<int:kpi_id>/", CriterionsCreateView.as_view(), name="criterion-create"),
    path("criterions/clauses/<int:criterion_id>/", CriterionDetailView.as_view(), name="criterion-detail"),
    path("criterions/delete/<int:criterion_id>/", CriterionDeleteView.as_view(), name="criterion-delete"),
    path("criterions/update/<int:criterion_id>/", CriterionUpdateView.as_view(), name="criterion-update"),

    path("clauses/create/<int:criterion_id>/", ClauseCreateView.as_view(), name="clause-create"),
    path("clauses/detatil/<int:clause_id>/", ClauseDetailView.as_view(), name="clause-detail"),
    path("clauses/delete/<int:clause_id>/", ClauseDeleteView.as_view(), name="clause-delete"),
    path("clauses/update/<int:clause_id>/", ClauseUpdateView.as_view(), name="clause-update"),
    path("clauses/create/internal/<int:parent_clause_id>/", ClauseInternalCreateView.as_view(), name="clause-internal-create"),

    path("submissions/<kpi_id>/", SubmissionsView.as_view(), name="submissions"),
    path("submissions/create/<int:clause_id>/", SubmissionCreateView.as_view(), name="submission-create"),
    path("submissions/detail/<int:submission_id>/", SubmissionDetailView.as_view(), name="submission-detail"),
    path("submissions/update/<int:submission_id>/", SubmissionUpdateView.as_view(), name="submission-edit"),
    path("submissions/delete/<int:submission_id>/", SubmissionDeleteView.as_view(), name="submission-delete"),

    path("works/<int:kpi_id>/", WorksView.as_view(), name="works"),
    path("works/detail/<int:work_id>/", WorkDetailView.as_view(), name="work-detail"),
    path("assessment/<int:work_id>/", AssessmentView.as_view(), name="assessment"),

    path("departments/", DepartmentView.as_view(), name="departments"),
    path("departments/create/", DepartmentCreateView.as_view(), name="department-create"),
    path("departments/detail/<int:department_id>/", DepartmentDetailView.as_view(), name="department-detail"),
    path("departments/delete/<int:department_id>/", DepartmentDeleteView.as_view(), name="department-delete"),
    path("departments/update/<int:department_id>/", DepartmentUpdateView.as_view(), name="department-update"),

    path("employees/<int:department_id>/", EmployeeView.as_view(), name="employees"),

    path("notefications/", NoteficationView.as_view(), name="get-notefications"),
    path("notefications/<int:employee_id>/", SendNoteficationView.as_view(), name="notefications"),
    path("notefications/see/<int:notefication_id>/", SeeNoteficationView.as_view(), name="see-notefication"),
]
