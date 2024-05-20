from datetime import date
from django.core.exceptions import ValidationError
from django.db import models
from users.models import User


class KPI(models.Model):
    # primary fields
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    ball = models.PositiveIntegerField()
    start_date = models.DateField()
    end_date = models.DateField()
    is_active = models.BooleanField(default=True)

    # secondary fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.DO_NOTHING)

    def clean(self, *args, **kwargs):
        if self.start_date >= self.end_date:
            raise ValidationError("Tugash sanasi boshlanish sanasidan keyin boʻlishi kerak.")

    def __str__(self) -> str:
        return self.name


class Criterion(models.Model):
    # primary fields
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    ball = models.PositiveIntegerField()
    kpi = models.ForeignKey(KPI, on_delete=models.CASCADE, related_name='criterions')
    responsible_person = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='criterions')

    # secondary fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.DO_NOTHING)

    def clean(self, *args, **kwargs):
        # Check if the creation date is after the end date of the KPI

        if self.kpi.end_date and date.today() > self.kpi.end_date:
            raise ValidationError("Mezon yaratish sanasi KPI tugash sanasidan keyin boʻlishi mumkin emas.")
        
        # Calculate the sum of ball values of all existing criterions
        existing_criterion_balls_sum = self.kpi.criterions.exclude(pk=self.pk).aggregate(total_ball=models.Sum('ball'))['total_ball'] or 0
        
        # Add the ball of the new criterion
        new_criterion_ball = self.ball
        
        # Total ball after adding the new criterion
        total_ball_after_addition = existing_criterion_balls_sum + new_criterion_ball
        
        # Check if the total exceeds the KPI's ball
        if total_ball_after_addition > self.kpi.ball:
            raise ValidationError("Ushbu KPI ga tegishli barcha mezonlar bali yig'indisi KPI balidan kam yoki teng bo'lishi kerak.")

    def __str__(self):
        return self.name
    

class Clause(models.Model):
    # primary fields
    name = models.CharField(max_length=255)
    description = models.TextField()
    ball = models.PositiveIntegerField()
    does_the_system_give_mark = models.BooleanField(default=True)
    criterion = models.ForeignKey(Criterion, on_delete=models.CASCADE, related_name='clauses')
    kpi = models.ForeignKey(KPI, on_delete=models.CASCADE, related_name='clauses')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')

    # secondary fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.DO_NOTHING)

    def clean(self, *args, **kwargs):
        # Check if the creation date is after the end date of the KPI
        if self.criterion.kpi.end_date and date.today() > self.criterion.kpi.end_date:
            raise ValidationError("Band yaratish sanasi KPI tugash sanasidan keyin boʻlishi mumkin emas.")
        
        # Check if the parent clause belongs to the same criterion
        if self.parent and self.parent.criterion != self.criterion:
            raise ValidationError("Yuqori band va joriy band bir xil mezonga tegishli bo'lishi kerak.")

        if self.parent is None:
            # Calculate the sum of ball values of all existing clauses
            existing_clause_balls_sum = self.criterion.clauses.exclude(pk=self.pk).aggregate(total_ball=models.Sum('ball'))['total_ball'] or 0
            
            # Add the ball of the new clause
            new_clause_ball = self.ball
            
            # Total ball after adding the new clause
            total_ball_after_addition = existing_clause_balls_sum + new_clause_ball
            
            # Check if the total exceeds the criterion's ball
            if total_ball_after_addition > self.criterion.ball:
                raise ValidationError("Ushbu Mezonga tegishli barcha bandlar bali yig'indisi mezon balidan kam yoki teng bo'lishi kerak.")
        else:
            # Calculate the sum of ball values of all existing clauses
            existing_clause_balls_sum = self.parent.children.exclude(pk=self.pk).aggregate(total_ball=models.Sum('ball'))['total_ball'] or 0
            
            # Add the ball of the new clause
            new_clause_ball = self.ball
            
            # Total ball after adding the new clause
            total_ball_after_addition = existing_clause_balls_sum + new_clause_ball
            
            # Check if the total exceeds the criterion's ball
            if total_ball_after_addition > self.parent.ball:
                raise ValidationError("Ushbu Bandga tegishli barcha ichki bandlar bali yig'indisi mezon balidan kam yoki teng bo'lishi kerak.")

    def __str__(self) -> str:
        return self.name


class Submission(models.Model):
    # primary fields
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='submissions')
    clause = models.ForeignKey(Clause, on_delete=models.CASCADE, related_name='submissions')
    kpi = models.ForeignKey(KPI, on_delete=models.CASCADE, related_name='submissions')
    file = models.FileField(upload_to='submissions')
    comment = models.TextField()
    is_checked = models.BooleanField(default=False)
    is_marked = models.BooleanField(default=False)

    # secondary fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('owner', 'clause')

    def clean(self, *args, **kwargs):
        # Check if the creation date is after the end date of the KPI
        if self.clause.criterion.kpi.end_date and self.created_at > self.clause.criterion.kpi.end_date:
            raise ValidationError("Hisobot yaratish sanasi KPI tugash sanasidan keyin boʻlishi mumkin emas.")

    def __str__(self) -> str:
        return self.clause.name


class Result(models.Model):
    # primary fields
    kpi = models.ForeignKey(KPI, on_delete=models.CASCADE, related_name='results')
    employee = models.ForeignKey(User, on_delete=models.CASCADE, related_name='results')
    ball = models.PositiveIntegerField()

    # secondary fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('kpi', 'employee')

    def clean(self):
        # Check if the ball of result is less than or equal to the criterion's ball
        if self.criterion and self.ball > self.criterion.ball:
            raise ValidationError("Natija bali mezon balidan kam yoki unga teng bo'lishi kerak.")

        # Check if the creation date is after the end date of the KPI
        if self.kpi.end_date and self.created_at > self.kpi.end_date:
            raise ValidationError("Hodim KPI natijasini o'zgartirish sanasi KPI tugash sanasidan keyin boʻlishi mumkin emas.")

    def __str__(self):
        return self.employee.full_name


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
    # primary fields
    type = models.PositiveSmallIntegerField(choices=TYPE_CHOICES, default=SUCCESS)
    massage = models.TextField()
    receiver = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='notefications')
    sender = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='messages')
    unread = models.BooleanField(default=True)

    # secondary fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.massage[:100]
