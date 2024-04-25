from django import forms
from .models import KPI, Metric, Submission


class KPICreationForm(forms.ModelForm):

    class Meta:
        model = KPI
        fields = "__all__"


class MetricCreationForm(forms.ModelForm):

    class Meta:
        model = Metric
        fields = "__all__"


class SubmissionCreationForm(forms.ModelForm):

    class Meta:
        model = Submission
        fields = "__all__"
