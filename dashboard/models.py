from django.db import models
from users.models import User


class Department(models.Model):
    name = models.CharField(max_length=255, unique=True)
    responsible_employee = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    employees = models.ManyToManyField(User, related_name='employees')

    def __str__(self) -> str:
        return self.name
    

class KPI(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    total_ball = models.PositiveIntegerField()
    responsible_employee = models.ForeignKey(User, on_delete=models.DO_NOTHING) # Manager | prorector

    def __str__(self) -> str:
        return self.name
    
    
class Metric(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    ball = models.PositiveIntegerField()
    deadline = models.DateField()

    kpi = models.ForeignKey(KPI, on_delete=models.CASCADE, related_name='metrics')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')

    def __str__(self) -> str:
        return self.name


class Result(models.Model):
    kpi = models.ForeignKey(KPI, on_delete=models.CASCADE)
    employee = models.ForeignKey(User, on_delete=models.CASCADE, related_name='results')
    total_ball = models.PositiveIntegerField()


class Submission(models.Model):
    employee = models.ForeignKey(User, on_delete=models.CASCADE, related_name='submissions')
    manager = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    metric = models.ForeignKey(Metric, on_delete=models.CASCADE, related_name='submissions')
    file = models.FileField(upload_to='submissions')
    comment = models.TextField()
    ball = models.PositiveIntegerField(blank=True)
    submitted_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.employee.username

    def save(self, *args, **kwargs):
        if not self.pk:  # If this is a new submission
            if not self.ball and self.metric:
                self.ball = self.metric.ball

            try:
                result = self.employee.results.get(kpi=self.metric.kpi)
                result.total_ball += self.ball
                result.save()
            except Result.DoesNotExist:
                result = Result(kpi=self.metric.kpi, employee=self.employee, total_ball=self.ball)
                result.save()
        else:  # If this is an update to an existing submission
            prev_instance = Submission.objects.get(pk=self.pk)
            if prev_instance.ball != self.ball:
                try:
                    result = self.employee.results.get(kpi=self.metric.kpi)
                    result.total_ball += (self.ball - prev_instance.ball)
                    result.save()
                except Result.DoesNotExist:
                    pass

        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        try:
            result = Result.objects.get(kpi=self.metric.kpi, employee=self.employee)
            result.total_ball -= self.ball
            result.save()
        except Result.DoesNotExist:
            pass

        super().delete(*args, **kwargs)


class Notefication(models.Model):
    massage = models.TextField()
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notefications')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='messages')
    unread = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.massage[:100]
