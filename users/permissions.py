from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import redirect
from .models import User


class BaseUserPassesTestMixin(UserPassesTestMixin):
    """
    Base permission.
    """
    def handle_no_permission(self):
        return redirect("landing_page")


class IsAdmin(BaseUserPassesTestMixin):
    """
    Custom permission to only allow CEOs to access the view.
    """
    def test_func(self):
        # Check if the user has a CEO role
        return self.request.user.role == User.ADMIN


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


class IsGuest(BaseUserPassesTestMixin):
    """
    Custom permission to only allow GUESTs to access the view.
    """
    def test_func(self):
        # Check if the user has GUESTs role
        return self.request.user.role == User.GUEST


class IsStaff(BaseUserPassesTestMixin):
    """
    Custom permission to only allow GUESTs to access the view.
    """
    def test_func(self):
        # Check if the user has GUESTs role
        return self.request.user.role != User.GUEST


class IsCeoOrManager(BaseUserPassesTestMixin):
    """
    Custom permission to only allow CEO or Manger to access the view.
    """
    def test_func(self):
        # Check if the user has CEO or Manger role
        return self.request.user.role == User.CEO or self.request.user.role == User.MANAGER
