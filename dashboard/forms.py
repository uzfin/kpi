from django import forms
from .models import KPI


class KPICreationForm(forms.ModelForm):

    class Meta:
        model = KPI
        fields = "__all__"
        