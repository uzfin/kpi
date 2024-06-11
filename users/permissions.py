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
        return not self.request.user.is_anonymous and self.request.user.role == User.ADMIN


class IsCEO(BaseUserPassesTestMixin):
    """
    Custom permission to only allow CEOs to access the view.
    """
    def test_func(self):
        # Check if the user has a CEO role
        return not self.request.user.is_anonymous and self.request.user.role == User.CEO


class IsManager(BaseUserPassesTestMixin):
    """
    Custom permission to only allow MANAGERs to access the view.
    """
    def test_func(self):
        # Check if the user has a MANAGERs role
        return not self.request.user.is_anonymous and self.request.user.role == User.MANAGER


class IsBoss(BaseUserPassesTestMixin):
    """
    Custom permission to only allow BOSSs to access the view.
    """
    def test_func(self):
        # Check if the user has BOSSs role
        return not self.request.user.is_anonymous and self.request.user.role == User.BOSS


class IsEmployee(BaseUserPassesTestMixin):
    """
    Custom permission to only allow EMPLOYEEs to access the view.
    """
    def test_func(self):
        # Check if the user has EMPLOYEEs role
        return not self.request.user.is_anonymous and self.request.user.role == User.EMPLOYEE


class IsGuest(BaseUserPassesTestMixin):
    """
    Custom permission to only allow GUESTs to access the view.
    """
    def test_func(self):
        # Check if the user has GUESTs role
        return not self.request.user.is_anonymous and self.request.user.role == User.GUEST


class IsStaff(BaseUserPassesTestMixin):
    """
    Custom permission to only allow GUESTs to access the view.
    """
    def test_func(self):
        # Check if the user has GUESTs role
        return not self.request.user.is_anonymous and self.request.user.role != User.GUEST


class IsACM(BaseUserPassesTestMixin):
    """
    Custom permission to only allow Admin, Ceo, Manager to access the view.
    """
    def test_func(self):
        # Check if the user has CEO or Manger role
        if not self.request.user.is_anonymous:
            role = self.request.user.role
            return role == User.ADMIN or role == User.CEO or role == User.MANAGER
        return False
