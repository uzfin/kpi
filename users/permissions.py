from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import redirect
from .models import User


class BaseUserPassesTestMixin(UserPassesTestMixin):
    """
    Base permission.
    """
    def handle_no_permission(self):
        return redirect("landing_page")


class IsCEO(BaseUserPassesTestMixin):
    """
    Custom permission to only allow CEOs to access the view.
    """
    def test_func(self):
        # Check if the user has a CEO role
        return self.request.user.role == User.CEO


class IsManager(BaseUserPassesTestMixin):
    """
    Custom permission to only allow MANAGERs to access the view.
    """
    def test_func(self):
        # Check if the user has a MANAGERs role
        return self.request.user.role == User.MANAGER


class IsEmployee(BaseUserPassesTestMixin):
    """
    Custom permission to only allow EMPLOYEEs to access the view.
    """
    def test_func(self):
        # Check if the user has EMPLOYEEs role
        return self.request.user.role == User.EMPLOYEE


class IsCeoOrManager(BaseUserPassesTestMixin):
    """
    Custom permission to only allow Ceo or Managers to access the view.
    """
    def test_func(self):
        # Check if the user has Ceo or Managers role
        return self.request.user.role == User.CEO or self.request.user.role == User.MANAGER


class IsCeoOrEmployee(BaseUserPassesTestMixin):
    """
    Custom permission to only allow Ceo or Employees to access the view.
    """
    def test_func(self):
        # Check if the user has Ceo or Employees role
        return self.request.user.role == User.CEO or self.request.user.role == User.EMPLOYEE


class IsManagerOrEmployee(BaseUserPassesTestMixin):
    """
    Custom permission to only allow Manager or Employees to access the view.
    """
    def test_func(self):
        # Check if the user has Manager or Employees role
        return self.request.user.role == User.MANAGER or self.request.user.role == User.EMPLOYEE
