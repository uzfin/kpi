from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import redirect
from .models import User


class IsCEO(UserPassesTestMixin):
    """
    Custom permission to only allow CEOs to access the view.
    """
    def test_func(self):
        # Check if the user has a CEO role
        return self.request.user.role == User.CEO

    def handle_no_permission(self):
        return redirect("users:login")


class IsManager(UserPassesTestMixin):
    """
    Custom permission to only allow MANAGERs to access the view.
    """
    def test_func(self):
        # Check if the user has a MANAGERs role
        return self.request.user.role == User.MANAGER

    def handle_no_permission(self):
        return redirect("users:login")


class IsEmployee(UserPassesTestMixin):
    """
    Custom permission to only allow EMPLOYEEs to access the view.
    """
    def test_func(self):
        # Check if the user has EMPLOYEEs role
        return self.request.user.role == User.EMPLOYEE

    def handle_no_permission(self):
        return redirect("users:login")


class IsCeoOrManager(UserPassesTestMixin):
    """
    Custom permission to only allow Ceo or Managers to access the view.
    """
    def test_func(self):
        # Check if the user has Ceo or Managers role
        return self.request.user.role == User.CEO or self.request.user.role == User.MANAGER

    def handle_no_permission(self):
        return redirect("users:login")