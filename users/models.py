from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ObjectDoesNotExist


class User(AbstractUser):
    ADMIN    = 0
    CEO      = 1
    MANAGER  = 2
    EMPLOYEE = 3
    BOSS     = 4
    GUEST    = 5

    ROLE_CHOICES = (
        (ADMIN, 'Admin'),
        (CEO, 'Direktor'),
        (MANAGER, 'Nazoratchi'),
        (EMPLOYEE, 'Hodim'),
        (BOSS, 'Bo\'lim boshlig\'i'),
        (GUEST, 'Mehmon'),
    )
    role = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, blank=True, null=True, default=GUEST)
    profile_picture = models.ImageField(upload_to='profile_pictures/', default='profile_pictures/default.png')
    phone = models.CharField(max_length=14, blank=True, null=True)

    @property
    def full_name(self):
        if self.get_full_name():
            return self.get_full_name()
        return self.username

    def __str__(self):
        return self.full_name
    

class Department(models.Model):
    # primary fields
    name = models.CharField(max_length=255, unique=True)
    boss = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='departments')
    employees = models.ManyToManyField(User, related_name='working_departments')

    # secondary fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.DO_NOTHING)

    def __str__(self) -> str:
        return self.name
