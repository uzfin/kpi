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

    @property
    def full_name(self):
        return self.get_full_name()

    def get_kpi_status(self, kpi):
        ball = 0
        try:
            ball = self.results.get(kpi=kpi).total_ball
        except ObjectDoesNotExist:
            pass

        return {
            "id": kpi.id,
            "name": kpi.name,
            "total": kpi.total_ball,
            "ball": ball,
            "percent": round(ball / kpi.total_ball * 100, 2)
        }
