from django import forms
from .models import KPI, Metric, Submission, Notefication, Mark


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


class SubmissionUpdationForm(forms.ModelForm):

    class Meta:
        model = Submission
        fields = ['file', 'comment']


class NoteficationCreationForm(forms.ModelForm):

    class Meta:
        model = Notefication
        fields = "__all__"


class MarkForm(forms.ModelForm):
    
    class Meta:
        model = Mark
        fields = "__all__"
