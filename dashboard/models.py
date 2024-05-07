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

    class Meta:
        unique_together = ('kpi', 'employee')

    def __str__(self):
        return self.employee.full_name
    

class Submission(models.Model):
    employee = models.ForeignKey(User, on_delete=models.CASCADE, related_name='submissions')
    metric = models.ForeignKey(Metric, on_delete=models.CASCADE, related_name='submissions')
    file = models.FileField(upload_to='submissions')
    comment = models.TextField()
    submitted_at = models.DateTimeField(auto_now=True)
    is_checked = models.BooleanField(default=False)
    is_marked = models.BooleanField(default=False)

    class Meta:
        unique_together = ('metric', 'employee')

    def __str__(self) -> str:
        return self.employee.username


class Mark(models.Model):
    submission = models.OneToOneField(Submission, on_delete=models.CASCADE, related_name='mark')
    manager = models.ForeignKey(User, on_delete=models.CASCADE, related_name='marks', null=True, blank=True)
    ball = models.PositiveIntegerField()
    comment = models.TextField()
    marked_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.submission.employee.full_name


class Notefication(models.Model):
    SUCCESS = 1
    INFO = 2
    DENGER = 3
    WARNING = 4
    
    TYPE_CHOICES = (
        (SUCCESS, "Rag'batlantirish"),
        (INFO, "Ma'lumot berish"),
        (DENGER, 'Tanqid qilish'),
        (WARNING, 'Ogohlantirish'),
    )
    type = models.PositiveSmallIntegerField(choices=TYPE_CHOICES, default=SUCCESS)
    massage = models.TextField()
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notefications')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='messages')
    unread = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.massage[:100]
