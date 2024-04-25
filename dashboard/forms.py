from django import forms
from .models import KPI, Metric


class KPICreationForm(forms.ModelForm):

    class Meta:
        model = KPI
        fields = "__all__"


class MetricCreationForm(forms.ModelForm):

    class Meta:
        model = Metric
        fields = "__all__"
