from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    CEO = 1
    MANAGER = 2
    EMPLOYEE = 3
    
    ROLE_CHOICES = (
        (CEO, 'Rector'),
        (MANAGER, 'Prorector'),
        (EMPLOYEE, 'Employee'),
    )
    role = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, blank=True, null=True, default=EMPLOYEE)
    profile_picture = models.ImageField(upload_to='profile_pictures/', default='profile_pictures/default.jpg')

    @property
    def full_name(self):
        return self.get_full_name()
