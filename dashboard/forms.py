from django import forms
from .models import KPI, Criterion, Clause


class KPICreationForm(forms.ModelForm):

    class Meta:
        model = KPI
        fields = "__all__"


class CriterionCreationForm(forms.ModelForm):

    class Meta:
        model = Criterion
        fields = "__all__"


class ClauseCreationForm(forms.ModelForm):

    class Meta:
        model = Clause
        fields = "__all__"


# class SubmissionCreationForm(forms.ModelForm):

#     class Meta:
#         model = Submission
#         fields = "__all__"


# class SubmissionUpdationForm(forms.ModelForm):

#     class Meta:
#         model = Submission
#         fields = ['file', 'comment']


# class NoteficationCreationForm(forms.ModelForm):

#     class Meta:
#         model = Notefication
#         fields = "__all__"


# class MarkForm(forms.ModelForm):
    
#     class Meta:
#         model = Mark
#         fields = "__all__"
