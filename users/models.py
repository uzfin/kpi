from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ObjectDoesNotExist


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

    @classmethod
    def employee_kpi_status(cls, kpis):
        data = []
        for employee in cls.objects.filter(role=cls.EMPLOYEE):
            em_data = []
            for kpi in kpis:
                em_data.append(employee.get_kpi_status(kpi))
            data.append(em_data)

        return data
